#!/usr/bin/env python3
import sys
import numpy as np
from qtpy.QtCore import QObject, QThread, Signal
from qtpy.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.ticker import StrMethodFormatter
import matplotlib.pyplot as plt

from siriushlacon.mks937b.consts import data
from siriushlacon.utils.consts import BO, SI, TB, TS

from epics import PV

import random
import time
import atexit
import re
import logging
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
                labels.append(gauge.pressurePV.pvname)

            with dataLock:
                self.window.data = data
                self.window.labels = labels

            self.comm.doRefresh.emit()

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

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.macros = {'TYPE':BO}
        self.comm = Comm()
        self.gauges = []
        self.comm.doRefresh.connect(self.plot)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # self.toolbar = NavigationToolbar(self.canvas, self)

        # set the layout
        layout = QVBoxLayout()
        # layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.bar_width = 0.25
        self.title = "Booster Pressure"

        self.load_pvs()

        # Init worker thread
        self.workerThread = WorkingThread(comm=self.comm, window=self)
        self.workerThread.start()

        atexit.register(self.cleanup)

    def load_pvs(self):
        ch_reg = re.compile(r':[A-C][0-9]')
        for d_row in data:
            if d_row.enable:
                i = 0
                for ch_prefix in d_row.channel_prefix[:4]:
                    # if i >= 5:
                    #     # Filter out PR
                    #     continue
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

    def autolabel(self, bars, ax):
        """ Attach a text label above each bar in , displaying its height. """
        for bar in bars:
            height = bar.get_height()
            ax.annotate('{:.2e}'.format(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points", ha='center', va='bottom')

    def plot(self):
        # random data
        with dataLock:
            self.figure.clear()

            # create an axis
            ax = self.figure.add_subplot()
            x = np.arange(len(self.labels))

            bars = ax.bar(x, self.data, self.bar_width)
            ax.set_title(self.title)
            ax.grid(which='both')
            ax.grid(which='major', alpha=0.5, linestyle='-')
            ax.grid(which='minor', alpha=0.3, linestyle='--')

            ax.set_yscale('log')
            ax.set_ylabel('mBar')

            ax.set_xticks(x)
            ax.set_xticklabels(self.labels)

            self.autolabel(bars, ax)

            # refresh canvas
            self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())