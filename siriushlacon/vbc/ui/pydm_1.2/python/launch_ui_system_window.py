#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from pydm import Display

import json

class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(parent=parent, args=args, macros=macros)

        # defining macro for PyDMRelatedDisplayButton (for opening "advanced_window.ui")
        self.Advance_tab.macros = json.dumps({"IOC":"$IOC"})
        # defining macro for PyDMRelatedDisplayButton (for opening "simple_window.ui")
        self.Simple_tab.macros = json.dumps({"IOC":"$IOC"})
        # defining macro for PyDMRelatedDisplayButton (for opening "warning_message.ui")
        self.Shell_warning_message.macros = json.dumps({"IOC":"$IOC"})

    def ui_filename(self):
        return '../ui/latest/system_window.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
