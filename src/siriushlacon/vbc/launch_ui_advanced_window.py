#!/usr/bin/env python3
from pydm import Display
from siriushlacon.vbc.consts import ADVANCED_WINDOW_UI, CONFIRMATION_MESSAGE_PY

import json


class DeviceMenu(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=ADVANCED_WINDOW_UI
        )

        # defining macros for PyDMShellCommand (valve open/close confirmation)
        macros_ioc = macros["IOC"]
        RELAY_SH_STR = f"pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {CONFIRMATION_MESSAGE_PY} {macros_ioc}"

        self.Relay1.commands = [f"{RELAY_SH_STR} 1"]
        self.Relay2.commands = [f"{RELAY_SH_STR} 2"]
        self.Relay3.commands = [f"{RELAY_SH_STR} 3"]
        self.Relay4.commands = [f"{RELAY_SH_STR} 4"]
        self.Relay5.commands = [f"{RELAY_SH_STR} 5"]

        self.Relay1.macros = json.dumps(
            {"IOC": macros_ioc, "RELAY": "1", "VALVE": "Valve 1?"}
        )
        self.Relay2.macros = json.dumps(
            {"IOC": macros_ioc, "RELAY": "2", "VALVE": "Pre-vacuum Valve?"}
        )
        self.Relay3.macros = json.dumps(
            {"IOC": macros_ioc, "RELAY": "3", "VALVE": "Valve 3?"}
        )
        self.Relay4.macros = json.dumps(
            {"IOC": macros_ioc, "RELAY": "4", "VALVE": "Gate Valve?"}
        )
        self.Relay5.macros = json.dumps(
            {"IOC": macros_ioc, "RELAY": "venting_valve", "VALVE": "Venting Valve?"}
        )
