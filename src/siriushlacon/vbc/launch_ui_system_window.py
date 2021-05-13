#!/usr/bin/env python3

import json
from qtpy.QtGui import QPixmap
from pydm import Display
from siriushlacon.vbc.consts import (
    ADVANCED_WINDOW_PY,
    CHECK_PRESSURE_SCRIPT,
    OK_MESSAGE_PY,
    PLAY_IMG,
    PROCESS_OFF_SCRIPT,
    PROCESS_ON_SCRIPT,
    SIMPLE_WINDOW_PY,
    STOP_IMG,
    SYSTEM_WINDOW_UI,
    WARNING_WINDOW_PY,
)


class DeviceMenu(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=SYSTEM_WINDOW_UI
        )
        self.lblOn.setPixmap(QPixmap(PLAY_IMG))
        self.lblOff.setPixmap(QPixmap(STOP_IMG))

        macros_ioc = macros["IOC"]

        self.btnSimpleTab.macros = json.dumps({"IOC": macros_ioc})
        self.btnSimpleTab.filenames = [SIMPLE_WINDOW_PY]

        # self.label_40.setPixmap(QPixmap(STOP_IMG))
        self.Advanced_tab.macros = json.dumps({"IOC": macros_ioc})
        self.Advanced_tab.filenames = [ADVANCED_WINDOW_PY]

        self.Shell6.commands = [f"python {CHECK_PRESSURE_SCRIPT} {macros_ioc} 0"]

        self.Shell5.commands = [f"python {PROCESS_OFF_SCRIPT} {macros_ioc}"]

        self.Shell_PV_trigger_ON_2.commands = [
            f"python {PROCESS_ON_SCRIPT} {macros_ioc}"
        ]

        self.Shell3.commands = [
            f"pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {OK_MESSAGE_PY} {macros_ioc}"
        ]
        self.Shell_PV_trigger_PRESSURIZED_2.commands = [
            f"pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {WARNING_WINDOW_PY} {macros_ioc}"
        ]
