#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from qtpy.QtGui import QPixmap
from pydm import Display
from siriushlacon.vbc.consts import (
    ADVANCED_WINDOW_PY,
    CHECK_PRESSURE_SCRIPT,
    COMMUTE_VALVE_SCRIPT,
    OK_MESSAGE_PY,
    PROCESS_OFF_SCRIPT,
    PROCESS_ON_SCRIPT,
    SYSTEM_WINDOW_UI,
    WARNING_WINDOW_PY,
    CONFIRMATION_MESSAGE_PY,
    STOP_IMG,
    SIMPLE_WINDOW_PY,
    PLAY_IMG,
)


class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=SYSTEM_WINDOW_UI
        )
        self.lblOn.setPixmap(QPixmap(PLAY_IMG))
        self.lblOff.setPixmap(QPixmap(STOP_IMG))

        self.btnSimpleTab.macros = json.dumps({"IOC": macros["IOC"]})
        self.btnSimpleTab.filenames = [SIMPLE_WINDOW_PY]

        # self.label_40.setPixmap(QPixmap(STOP_IMG))
        self.Advanced_tab.macros = json.dumps({"IOC": macros["IOC"]})
        self.Advanced_tab.filenames = [ADVANCED_WINDOW_PY]
        self.Shell6.commands = [
            "python {} {} 0".format(CHECK_PRESSURE_SCRIPT, macros["IOC"])
        ]
        self.Shell5.commands = [
            "python {} {}".format(PROCESS_OFF_SCRIPT, macros["IOC"])
        ]
        self.Shell3.commands = [
            "pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {} {}".format(
                OK_MESSAGE_PY, macros["IOC"]
            )
        ]
        self.Shell_PV_trigger_PRESSURIZED_2.commands = [
            "pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {} {}".format(
                WARNING_WINDOW_PY, macros["IOC"]
            )
        ]
        self.Shell_PV_trigger_ON_2.commands = [
            "python {} {}".format(PROCESS_ON_SCRIPT, macros["IOC"])
        ]
