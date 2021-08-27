#!/usr/bin/env python3
import logging
import re
from typing import List

import conscommon.data_model
from pydm import Display
from pydm.widgets.drawing import PyDMDrawingRectangle
from pydm.widgets.label import PyDMLabel
from qtpy.QtCore import QRect, Qt
from qtpy.QtGui import QBrush, QColor, QFont
from qtpy.QtWidgets import QFrame, QLabel

from siriushlacon.agilent4uhv.consts import lazy_devices
from siriushlacon.utils.consts import BO, OVERVIEW_UI, SI, TB, TS
from siriushlacon.widgets.layout import FlowLayout

logger = logging.getLogger()


class PVInfo:
    def __init__(
        self, PV: str, DISP: str, ALARM: str, SEC: str, RACK: str, RS485: str
    ) -> None:
        self.PV: str = PV
        self.DISP: str = DISP
        self.ALARM: str = ALARM
        self.SEC: str = SEC
        self.RACK: str = RACK
        self.RS485: str = RS485

    def __str__(self) -> str:
        return f"PVInfo({self.__dict__})"


class Overview(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(Overview, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=OVERVIEW_UI
        )

        self.ch_reg = re.compile(r":[C][0-9]")
        self._devices = lazy_devices.get()
        self.pv_info_list: List[PVInfo] = []
        for device in self._devices:
            if not device.enable:
                continue
            for channel in device.channels:
                self.load_pv_dict(device, channel)

        self.mainArea.setWidgetResizable(True)
        layout = FlowLayout(self.scrollAreaContent)
        for pv_info in self.pv_info_list:
            layout.addWidget(self.get_gauge(None, pv_info=pv_info))

    def load_pv_dict(
        self,
        device: conscommon.data_model.Device,
        channel: conscommon.data_model.Channel,
    ):
        if (
            (self.ch_reg.match(channel.prefix[-3:]))
            or (self.macros().get("TYPE") == BO and not channel.prefix.startswith(BO))
            or (self.macros().get("TYPE") == SI and not channel.prefix.startswith(SI))
            or (self.macros().get("TYPE") == TS and not channel.prefix.startswith(TS))
            or (self.macros().get("TYPE") == TB and not channel.prefix.startswith(TB))
        ):
            logger.info("Ignored {}".format(channel.prefix))
            return None

        self.pv_info_list.append(
            PVInfo(
                PV=channel.prefix + ":Pressure-Mon",
                DISP=channel.prefix + ":Pressure-Mon",
                ALARM=channel.prefix + ":Pressure-Mon.STAT",
                SEC=device.info.sector,
                RACK=device.info.rack,
                RS485=device.info.serial_id,
            )
        )

    def get_gauge(self, parent, pv_info: PVInfo):
        tooltip = "".join(
            [f"{key}\t{value}\n" for key, value in pv_info.__dict__.items()]
        )

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
        alarmRec.channel = "ca://{}".format(pv_info.ALARM)
        alarmRec.setGeometry(QRect(0, 0, width, height))
        alarmRec.setToolTip(tooltip)
        alarmRec.setProperty("alarmSensitiveContent", True)
        alarmRec.setProperty("brush", brush)
        alarmRec.setObjectName("alarmRec")
        # alarmRec.setStyleSheet("margin:5px; border:3px solid rgb(0, 0, 0);")

        lblName = QLabel(frame)
        lblName.setGeometry(QRect(width * 0.05, 50, width - width * 0.05, 20))
        font = QFont()
        font.setPointSize(12)
        lblName.setFont(font)
        lblName.setAlignment(Qt.AlignCenter)
        lblName.setText("{}".format(pv_info.DISP))
        lblName.setObjectName("lblName")
        lblName.setToolTip(tooltip)

        lblVal = PyDMLabel(frame)
        lblVal.setGeometry(QRect(width * 0.05, 10, width - width * 0.05, 30))
        font = QFont()
        font.setPointSize(18)
        lblVal.setFont(font)
        lblVal.setToolTip(tooltip)
        lblVal.setAlignment(Qt.AlignCenter)
        lblVal.setProperty("showUnits", False)
        lblVal.setObjectName("lblVal")
        lblVal.channel = "ca://{}".format(pv_info.PV)
        lblVal.precisionFromPV = False
        lblVal.precision = 2
        if self.macros().get("FORMAT", "") == "EXP":
            lblVal.displayFormat = PyDMLabel.DisplayFormat.Exponential
        return frame
