#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from pydm import Display
import sys

import json

class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(parent=parent, args=args, macros=macros)

        # defining macros for PyDMShellCommand (valve open/close confirmation)
        self.Relay1.macros = json.dumps({"IOC":"$IOC", "RELAY":"1", "VALVE":"Valve 1?"})
        self.Relay2.macros = json.dumps({"IOC":sys.argv[2], "RELAY":"2", "VALVE":"Pre-vacuum Valve?"})
        self.Relay3.macros = json.dumps({"IOC":"$IOC", "RELAY":"3", "VALVE":"Valve 3?"})
        self.Relay4.macros = json.dumps({"IOC":"$IOC", "RELAY":"4", "VALVE":"Gate Valve?"})
        self.Relay5.macros = json.dumps({"IOC": "$IOC", "RELAY":"venting_valve","VALVE":"Venting Valve?"})

    def ui_filename(self):
        #return '../ui/latest/advanced_window.ui'
        return 'advanced_window.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
