#!/usr/local/env python3
import json
import logging

from pydm import Display
from pydm.widgets.related_display_button import PyDMRelatedDisplayButton
from qtpy.QtWidgets import QWidget, QVBoxLayout

from siriushlacon.pctrl.consts import IOCS_JSON, PCTRL_UI


def load_iocs():
    with open(IOCS_JSON, "rb") as f:
        iocs = json.load(f)
    return iocs


logger = logging.getLogger()


class Main(Display):
    def __init__(self, parent=None):
        super().__init__(parent=parent, ui_filename=PCTRL_UI)
        self.iocs = load_iocs()
        self.areas = set([e["area"] for e in self.iocs])
        self.tabs = {}
        self.init_layout()

    def init_layout(self):
        for area in self.areas:
            self.tabs[area] = QWidget()
            self.tabs[area].setLayout(QVBoxLayout())
            self.tabWidget.addTab(self.tabs[area], area)

        for ioc in self.iocs:
            button = PyDMRelatedDisplayButton(ioc["desc"])
            button.filenames = ["ui/procServControl.ui"]
            button.macros = '{"P":"' + ioc["pv"] + '"}'
            button.showIcon = False
            button.openInNewWindow = True
            self.tabs[ioc["area"]].layout().addWidget(button)

        for area in self.areas:
            self.tabs[area].layout().addStretch(0)
