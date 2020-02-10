#!/usr/bin/env python3
import logging
import re

from pydm import Display
from pydm.widgets.drawing import PyDMDrawingRectangle
from pydm.widgets.label import PyDMLabel
from qtpy.QtCore import Qt, QRect
from qtpy.QtGui import QBrush, QColor, QFont
from qtpy.QtWidgets import QFrame, QLabel

from siriushlacon.agilent4uhv.consts import data
from siriushlacon.utils.consts import OVERVIEW_UI, BO, TB, TS, SI
from siriushlacon.utils.widgets import FlowLayout

logger = logging.getLogger()


class Overview(Display):

    def __init__(self, parent=None, args=None, macros=None):
        super(Overview, self).__init__(parent=parent, args=args, macros=macros)
        self.macros = macros
        self.pvs = []
        self.load_pvs()
        self.mainArea.setWidgetResizable(True)
        layout = FlowLayout(self.scrollAreaContent)
        for pv in self.pvs:
            layout.addWidget(self.get_gauge(None, macros=pv))

    def load_pvs(self):
        ch_reg = re.compile(r':[C][0-9]')
        ed_reg = re.compile(r'-BG')
        for d_row in data:
            if d_row.enable:
                for ch_prefix in d_row.channel_prefix:

                    if not ed_reg.match(ch_prefix[-3:]):
                        # Filter out readings that aren't -ED
                        continue

                    if self.macros.get('TYPE') == BO:
                        if  not ch_prefix.startswith(BO):
                            logger.info('Ignored {}'.format(ch_prefix))
                            continue

                    elif self.macros.get('TYPE') == SI:
                        if not ch_prefix.startswith(SI):
                            logger.info('Ignored {}'.format(ch_prefix))
                            continue
                        pass

                    elif self.macros.get('TYPE') == TS:
                        if not ch_prefix.startswith(TS):
                            logger.info('Ignored {}'.format(ch_prefix))
                            continue
                        pass

                    elif self.macros.get('TYPE') == TB:
                        if not ch_prefix.startswith(TB):
                            logger.info('Ignored {}'.format(ch_prefix))
                            continue
                        pass

                    else:
                        logger.info('Ignored {}'.format(ch_prefix))
                        logger.warning('Invalid type {}.'.format(self.macros.get('TYPE')))
                        continue

                    if ch_reg.match(ch_prefix[-3:]):
                        # Filter out unnused channels by it's name
                        continue

                    self.pvs.append({
                        'PV': ch_prefix + ':Pressure-Mon',
                        'DISP': ch_prefix + ':Pressure-Mon',
                        'ALARM': ch_prefix + ':Pressure-Mon.STAT',
                        'SEC.': d_row.sector,
                        'RACK': d_row.rack,
                        'RS485': d_row.rs485_id,
                        'IP': d_row.ip
                    })

    def get_gauge(self, parent, macros):
        aux = []
        for k, v in macros.items():
            aux.append('{}\t{}\n'.format(k, v))
        tooltip = ''.join(aux)

        width = 320
        height = 100

        frame = QFrame(parent)
        frame.setGeometry(QRect(10, 10, width, height))
        frame.setMinimumSize(width, height)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        frame.setObjectName("frame")

        brush = QBrush(QColor(180, 180, 180))
        brush.setStyle(Qt.NoBrush)

        alarmRec = PyDMDrawingRectangle(frame)
        alarmRec.channel = "ca://{}".format(macros.get('ALARM', None))
        alarmRec.setGeometry(QRect(0, 0, width, height))
        alarmRec.setToolTip(tooltip)
        alarmRec.setProperty("alarmSensitiveContent", True)
        alarmRec.setProperty("brush", brush)
        alarmRec.setObjectName("alarmRec")
        # alarmRec.setStyleSheet("margin:5px; border:3px solid rgb(0, 0, 0);")

        lblName = QLabel(frame)
        lblName.setGeometry(QRect(width*0.05, 50, width - width*0.05, 20))
        font = QFont()
        font.setPointSize(12)
        lblName.setFont(font)
        lblName.setAlignment(Qt.AlignCenter)
        lblName.setText("{}".format(macros.get('DISP', None)))
        lblName.setObjectName("lblName")
        lblName.setToolTip(tooltip)

        lblVal = PyDMLabel(frame)
        lblVal.setGeometry(QRect(width*0.05, 10, width - width*0.05, 30))
        font = QFont()
        font.setPointSize(18)
        lblVal.setFont(font)
        lblVal.setToolTip(tooltip)
        lblVal.setAlignment(Qt.AlignCenter)
        lblVal.setProperty("showUnits", False)
        lblVal.setObjectName("lblVal")
        lblVal.channel = "ca://{}".format(macros.get('PV', None))
        lblVal.precisionFromPV = False
        lblVal.precision = 2
        if self.macros.get('FORMAT', '') == 'EXP':
            lblVal.displayFormat = PyDMLabel.DisplayFormat.Exponential
        return frame

    def ui_filename(self):
        return OVERVIEW_UI

    def ui_filepath(self):
        return OVERVIEW_UI
