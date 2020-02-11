#!/usr/bin/env python3
import atexit
import logging
import numpy as np
import random
import re
import sys
import time

from epics import PV

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.ticker import StrMethodFormatter

from qtpy.QtCore import QObject, QThread, Signal
from qtpy.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from qtpy.QtGui import QDoubleValidator

from pydm import Display

from siriushlacon.mks937b.consts import data, MKS_GRAPH_UI
from siriushlacon.utils.consts import BO, SI, TB, TS

from threading import RLock

dataLock = RLock()

logger = logging.getLogger()


class Comm(QObject):
    doRefresh = Signal()
    stopRefresh = Signal()

class WorkingThread(QThread):
    def __init__(self, comm:Comm, window):
        super().__init__()
        self.comm = comm
        self.running = True
        self.comm.stopRefresh.connect(self.stop)
        self.window = window
    
    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            time.sleep(1)
            data = []
            labels = []

            for gauge in self.window.gauges:
                data.append(gauge.pressurePV.value)
                labels.append(gauge.channel)

            with dataLock:
                self.window.data = data
                self.window.labels = labels

            # self.comm.doRefresh.emit()

class Gauge:
    def __init__(self, channel:str, d_row):
        super().__init__()
        self.channel = channel
        self.device = d_row.device
        self.sector = d_row.sector
        self.rack = d_row.rack
        self.rs485_id = d_row.rs485_id
        self.ip = d_row.ip
        self.pressurePV = PV(self.channel + ":Pressure-Mon")

class Window(Display):
    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, ui_filename=MKS_GRAPH_UI)
        self.macros = macros
        # self.macros = {'TYPE':BO}
        self.type = self.macros['TYPE']

        self.comm = Comm()
        self.gauges = []
        self.labels = []
        self.data = []

        validator = QDoubleValidator()
        validator.setBottom(1e-11)
        validator.setDecimals(2)

        self.txtHihi.setValidator(validator)

        validator2 = QDoubleValidator()
        validator2.setBottom(1e-11)
        validator2.setDecimals(2)
        self.txtHigh.setValidator(validator2)
        
        self.btnHihi.clicked.connect(self.update_hihi)
        self.btnHigh.clicked.connect(self.update_high)

        self.hihi = 1e-07
        self.high = 1e-08

        self.txtHigh.setText(str(self.high))
        self.txtHihi.setText(str(self.hihi))

        # self.comm.doRefresh.connect(self.plot)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # self.toolbar = NavigationToolbar(self.canvas, self)

        # set the layout
        self.gridLayout.addWidget(self.canvas)

        self.bar_width = 0.25
        
        self.title = "{} Pressure".format(self.type)
        self.load_pvs()

        self.bars = []
        self.animation = FuncAnimation(fig=self.figure, func=self.plot, interval=10000)
        self.init_plot()
        self.plot()

        # Init worker thread
        self.workerThread = WorkingThread(comm=self.comm, window=self)
        self.workerThread.start()

        atexit.register(self.cleanup)

    def update_high(self):
        try:
            aux = float(self.txtHigh.text())
            if aux > self.hihi:
                self.txtHigh.setText(str(self.high))
            else:
                self.high = aux
                self.plot()
        except:
            logger.exception("Failed to parse {} to float.".format(self.txtHigh.text()))

    def update_hihi(self):
        try:
            aux = float(self.txtHihi.text())
            if aux < self.high:
                self.txtHihi.setText(str(self.hihi))
            else:
                self.hihi = aux 
                self.plot()
        except:
            logger.exception("Failed to parse {} to float.".format(self.txtHihi.text()))

    def load_pvs(self):
        ch_reg = re.compile(r':[A-C][0-9]')
        for d_row in data:
            if d_row.enable:
                i = 0
                for ch_prefix in d_row.channel_prefix[:4]:
                    if ch_reg.match(ch_prefix[-3:]):
                        # Filter out unnused channels by it's name
                        continue

                    if self.macros.get('TYPE') == BO:
                        if not ch_prefix.startswith(BO):
                            logger.info('Ignored {}'.format(ch_prefix))
                            continue
                    elif self.macros.get('TYPE') == TB:
                        if not ch_prefix.startswith(TB):
                            logger.info('Ignored {}'.format(ch_prefix))
                            continue
                    elif self.macros.get('TYPE') == SI:
                        if not ch_prefix.startswith(SI):
                            logger.info('Ignored {}'.format(ch_prefix))
                            continue
                    elif self.macros.get('TYPE') == TS:
                        if not ch_prefix.startswith(TS):
                            logger.info('Ignored {}'.format(ch_prefix))
                            continue
                    else:
                        logger.warning('Type {} not supported !'.format(self.macros.get('TYPE')))
                        logger.info('Ignored {}'.format(ch_prefix))
                        continue

                    self.gauges.append(Gauge(channel=ch_prefix, d_row=d_row))
                    i += 1
        self.gauges.sort(key=lambda x: x.channel, reverse=True)

    def cleanup(self):
        self.comm.stopRefresh.emit()

    def init_plot(self):
        self.figure.subplots_adjust(left=0.05, right=0.97, hspace=0, wspace=0, top=0.95)
        self.ax = self.figure.add_subplot(111)

    def autolabel(self, bars, ax):
        """ Attach a text label above each bar in , displaying its height. """
        for bar in bars:
            bar.set_edgecolor("#1f1f1f")
 
            if bar.get_height() >= self.high and bar.get_height() < self.hihi:
                bar.set_facecolor("y")
            elif bar.get_height() >= self.hihi:
                bar.set_facecolor("r")
            else:
                pass

            height = bar.get_height()
            ax.annotate('{:.1e}'.format(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points", ha='center', va='bottom')

    def plot(self, *args):
        # random data
        with dataLock:
            self.ax.clear()
            x = np.arange(len(self.labels))

            bars = self.ax.bar(x, self.data, self.bar_width)
            for tick in self.ax.get_xticklabels():
                tick.set_rotation(45)
                tick.set_ha('right')
            self.ax.set_title(self.title)
            self.ax.grid(which='both')
            self.ax.grid(which='major', alpha=0.5, linestyle='-')
            self.ax.grid(which='minor', alpha=0.3, linestyle='--')

            self.ax.set_yscale('log')
            self.ax.set_ylabel('mBar')

            self.ax.set_xticks(x)
            self.ax.set_xticklabels(self.labels)

            self.autolabel(bars, self.ax)

            # Limits
            self.ax.plot([-1, len(self.labels)+1], [self.hihi, self.hihi], linestyle='--', alpha=0.8, color='r')
            self.ax.plot([-1, len(self.labels)+1], [self.high, self.high], linestyle='--', alpha=0.8, color='y')

            # refresh canvas
            self.canvas.draw()

def showChart(macros:dict=None):
    main = Window(macros=macros)
    main.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    showChart({"TYPE":BO})

    sys.exit(app.exec_())