#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pydm import Display
from siriushlacon.vbc.consts import ADVANCED_WINDOW_UI

import json


class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=ADVANCED_WINDOW_UI
        )

        # defining macros for PyDMShellCommand (valve open/close confirmation)
        self.Relay1.macros = json.dumps(
            {"IOC": "$IOC", "RELAY": "1", "VALVE": "Valve 1?"}
        )
        self.Relay2.macros = json.dumps(
            {"IOC": sys.argv[2], "RELAY": "2", "VALVE": "Pre-vacuum Valve?"}
        )
        self.Relay3.macros = json.dumps(
            {"IOC": "$IOC", "RELAY": "3", "VALVE": "Valve 3?"}
        )
        self.Relay4.macros = json.dumps(
            {"IOC": "$IOC", "RELAY": "4", "VALVE": "Gate Valve?"}
        )
        self.Relay5.macros = json.dumps(
            {"IOC": "$IOC", "RELAY": "venting_valve", "VALVE": "Venting Valve?"}
        )
