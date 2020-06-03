#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pydm import Display
from siriushlacon.vbc.consts import ADVANCED_WINDOW_UI, CONFIRMATION_MESSAGE_PY

import json


class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=ADVANCED_WINDOW_UI
        )

        # defining macros for PyDMShellCommand (valve open/close confirmation)
        RELAY_SH_STR = "pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {} {}".format(
            CONFIRMATION_MESSAGE_PY, macros["IOC"]
        )
        self.Relay1.commands = [RELAY_SH_STR]
        self.Relay2.commands = [RELAY_SH_STR]
        self.Relay3.commands = [RELAY_SH_STR]
        self.Relay4.commands = [RELAY_SH_STR]
        self.Relay5.commands = [RELAY_SH_STR]

        self.Relay1.macros = json.dumps(
            {"IOC": macros["IOC"], "RELAY": "1", "VALVE": "Valve 1?"}
        )
        self.Relay2.macros = json.dumps(
            {"IOC": sys.argv[2], "RELAY": "2", "VALVE": "Pre-vacuum Valve?"}
        )
        self.Relay3.macros = json.dumps(
            {"IOC": macros["IOC"], "RELAY": "3", "VALVE": "Valve 3?"}
        )
        self.Relay4.macros = json.dumps(
            {"IOC": macros["IOC"], "RELAY": "4", "VALVE": "Gate Valve?"}
        )
        self.Relay5.macros = json.dumps(
            {"IOC": macros["IOC"], "RELAY": "venting_valve", "VALVE": "Venting Valve?"}
        )
