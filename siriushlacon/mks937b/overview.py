#!/usr/bin/python3
import logging
import re

from pydm import Display
from pydm.widgets.drawing import PyDMDrawingRectangle
from pydm.widgets.label import PyDMLabel
from qtpy.QtCore import Qt, QRect
from qtpy.QtGui import QBrush, QColor, QFont
from qtpy.QtWidgets import QFrame, QLabel

from siriushlacon.mks937b.consts import data
from siriushlacon.utils.consts import OVERVIEW_UI, BO, SI, TB, TS
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
            layout.addWidget(self.get_gauge(None, pv=pv))

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

                    self.pvs.append({
                        'PV': ch_prefix + ':Pressure-Mon-s',
                        'DISP': ch_prefix + ':Pressure-Mon',
                        'ALARM': ch_prefix + ':Pressure-Mon.STAT',
                        'DEVICE': d_row.device,
                        'SEC.': d_row.sector,
                        'RACK': d_row.rack,
                        'RS485': d_row.rs485_id,
                        'IP': d_row.ip
                    })
                    i += 1

    def get_gauge(self, parent, pv):
        aux = []
        for k, v in pv.items():
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
        alarmRec.channel = "ca://{}".format(pv.get('ALARM', None))
        alarmRec.setGeometry(QRect(0, 0, width, height*.8))
        alarmRec.setToolTip(tooltip)
        alarmRec.setProperty("alarmSensitiveContent", True)
        alarmRec.setProperty("brush", brush)
        alarmRec.setObjectName("alarmRec")
        # alarmRec.setStyleSheet(DRAW_ALARMS_NO_INVALID_QSS)

        alarmRecComm = PyDMDrawingRectangle(frame)
        alarmRecComm.channel = "ca://{}".format(
            pv.get('DEVICE', None) + ':Pressure:Read')
        alarmRecComm.setGeometry(QRect(0, height*.8, width, height*.2))
        alarmRecComm.setToolTip('Connection Indicator: {}\t{}'.format(
            'DEVICE', pv.get('DEVICE', None) + ':Pressure:Read'))
        alarmRecComm.setProperty("alarmSensitiveContent", True)
        alarmRecComm.setProperty("brush", brush)
        alarmRecComm.setObjectName("alarmRecComm")
        alarmRecComm.setStyleSheet("""
            border:1px solid rgb(214, 214, 214);
        """)

        lblName = QLabel(frame)
        lblName.setGeometry(QRect(width*0.05, 50, width - width*0.05, 20))
        font = QFont()
        font.setPointSize(12)
        lblName.setFont(font)
        lblName.setAlignment(Qt.AlignCenter)
        lblName.setText("{}".format(pv.get('DISP', None)))
        lblName.setObjectName("lblName")
        lblName.setToolTip(tooltip)

        font = QFont()
        font.setPointSize(12)

        lblComm = QLabel(frame)
        lblComm.setGeometry(QRect(10, 80, 190, 20))
        lblComm.setFont(font)
        lblComm.setAlignment(Qt.AlignCenter)
        lblComm.setText('COMM Status')
        lblComm.setObjectName("lblComm")
        lblComm.setToolTip('Communication status to device {}'.format(
            pv.get('DEVICE', '')))

        lblCommPv = PyDMLabel(frame)
        lblCommPv.setGeometry(QRect(150, 80, 190, 20))
        lblCommPv.setFont(font)
        lblCommPv.setToolTip('Communication status to device {}'.format(
            pv.get('DEVICE', '')))
        lblCommPv.setAlignment(Qt.AlignCenter)
        lblCommPv.setObjectName("lblCommPv")
        lblCommPv.channel = "ca://{}".format(
            pv.get('DEVICE', None) + ':Pressure:Read.STAT')

        lblVal = PyDMLabel(frame)
        lblVal.setGeometry(QRect(width*0.05, 10, width - width*0.05, 30))
        font = QFont()
        font.setPointSize(18)
        lblVal.setFont(font)
        lblVal.setToolTip(tooltip)
        lblVal.setAlignment(Qt.AlignCenter)
        lblVal.setProperty("showUnits", False)
        lblVal.setObjectName("lblVal")
        lblVal.channel = "ca://{}".format(pv.get('PV', None))
        lblVal.precisionFromPV = False
        lblVal.precision = 2
        if self.macros.get('FORMAT', '') == 'EXP':
            lblVal.displayFormat = PyDMLabel.DisplayFormat.Exponential
        return frame

    def ui_filename(self):
        return OVERVIEW_UI

    def ui_filepath(self):
        return OVERVIEW_UI
