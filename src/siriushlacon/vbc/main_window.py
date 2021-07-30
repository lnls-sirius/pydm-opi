#!/usr/bin/env python3
import json
import logging

from pydm import Display
from pydm.widgets.byte import PyDMByteIndicator
from pydm.widgets.related_display_button import PyDMRelatedDisplayButton
from PyQt5.QtWidgets import QPushButton
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QLabel

from siriushlacon import __version__
from siriushlacon.utils.images import CNPEM_PIXMAP, LNLS_PIXMAP
from siriushlacon.vbc.consts import MAIN_WINDOW_UI, SYSTEM_WINDOW_PY
from siriushlacon.vbc.warning_message import VBCWarningMessageDialog

_logger = logging.getLogger(__name__)


class VBCMainWindow(Display):
    def test(self, *args, **kwargs):
        _logger.info("modal openning ...")
        dialog = VBCWarningMessageDialog(
            parent=self,
            prefix="VBC1",
            macros={"IOC": "VBC1", "CAR": "1"},
        )
        dialog.setModal(True)
        dialog.open()

    def __init__(self, parent=None, args=None, macros=None):
        super(VBCMainWindow, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=MAIN_WINDOW_UI
        )
        btn = QPushButton()
        btn.setText("test button")
        btn.clicked.connect(self.test)
        self.children()[0].layout().addWidget(btn, 9, 4)

        self.lnlsLabel: QLabel
        self.labelVersion: QLabel
        self.cnpemLabel: QLabel

        self.VBC_car_1: PyDMRelatedDisplayButton
        self.VBC_car_2: PyDMRelatedDisplayButton
        self.VBC_car_3: PyDMRelatedDisplayButton
        self.VBC_car_4: PyDMRelatedDisplayButton
        self.VBC_car_5: PyDMRelatedDisplayButton
        self.VBC_car_6: PyDMRelatedDisplayButton
        self.VBC_car_7: PyDMRelatedDisplayButton
        self.VBC_car_8: PyDMRelatedDisplayButton
        self.VBC_car_9: PyDMRelatedDisplayButton
        self.VBC_car_10: PyDMRelatedDisplayButton

        self.LED_1: PyDMByteIndicator
        self.LED_2: PyDMByteIndicator
        self.LED_3: PyDMByteIndicator
        self.LED_4: PyDMByteIndicator
        self.LED_5: PyDMByteIndicator
        self.LED_6: PyDMByteIndicator
        self.LED_7: PyDMByteIndicator
        self.LED_8: PyDMByteIndicator
        self.LED_9: PyDMByteIndicator
        self.LED_10: PyDMByteIndicator

        self.lnlsLabel.setPixmap(LNLS_PIXMAP)
        self.lnlsLabel.setFixedSize(LNLS_PIXMAP.size())

        self.cnpemLabel.setPixmap(CNPEM_PIXMAP)
        self.cnpemLabel.setFixedSize(CNPEM_PIXMAP.size())

        self.labelVersion.setText(__version__)

        self.VBC_car_1.filenames = [SYSTEM_WINDOW_PY]
        self.VBC_car_2.filenames = [SYSTEM_WINDOW_PY]
        self.VBC_car_3.filenames = [SYSTEM_WINDOW_PY]
        self.VBC_car_4.filenames = [SYSTEM_WINDOW_PY]
        self.VBC_car_5.filenames = [SYSTEM_WINDOW_PY]
        self.VBC_car_6.filenames = [SYSTEM_WINDOW_PY]
        self.VBC_car_7.filenames = [SYSTEM_WINDOW_PY]
        self.VBC_car_8.filenames = [SYSTEM_WINDOW_PY]
        self.VBC_car_9.filenames = [SYSTEM_WINDOW_PY]
        self.VBC_car_10.filenames = [SYSTEM_WINDOW_PY]

        self.VBC_car_1.macros = json.dumps({"IOC": "VBC1", "CAR": "1"})
        self.VBC_car_2.macros = json.dumps({"IOC": "VBC2", "CAR": "2"})
        self.VBC_car_3.macros = json.dumps({"IOC": "VBC3", "CAR": "3"})
        self.VBC_car_4.macros = json.dumps({"IOC": "VBC4", "CAR": "4"})
        self.VBC_car_5.macros = json.dumps({"IOC": "VBC5", "CAR": "5"})
        self.VBC_car_6.macros = json.dumps({"IOC": "VBC6", "CAR": "6"})
        self.VBC_car_7.macros = json.dumps({"IOC": "VBC7", "CAR": "7"})
        self.VBC_car_8.macros = json.dumps({"IOC": "VBC8", "CAR": "8"})
        self.VBC_car_9.macros = json.dumps({"IOC": "VBC9", "CAR": "9"})
        self.VBC_car_10.macros = json.dumps({"IOC": "VBC10", "CAR": "10"})

        COLOR_RED = QColor(255, 0, 0)
        self.LED_1._disconnected_color = COLOR_RED
        self.LED_2._disconnected_color = COLOR_RED
        self.LED_3._disconnected_color = COLOR_RED
        self.LED_4._disconnected_color = COLOR_RED
        self.LED_5._disconnected_color = COLOR_RED
        self.LED_6._disconnected_color = COLOR_RED
        self.LED_7._disconnected_color = COLOR_RED
        self.LED_8._disconnected_color = COLOR_RED
        self.LED_9._disconnected_color = COLOR_RED
        self.LED_10._disconnected_color = COLOR_RED
