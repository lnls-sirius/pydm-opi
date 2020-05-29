#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pydm import Display
from siriushlacon.vbc.consts import SYSTEM_WINDOW_UI, ADVANCED_WINDOW_UI


class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=SYSTEM_WINDOW_UI
        )

        # defining macro for PyDMRelatedDisplayButton (for opening "advanced_window.ui")
        self.Advance_tab.macros = json.dumps({"IOC": "$IOC"})
        self.Advance_tab.filename = ADVANCED_WINDOW_UI
        # defining macro for PyDMRelatedDisplayButton (for opening "warning_message.ui")
        self.Shell_warning_message.macros = json.dumps({"IOC": "$IOC"})
