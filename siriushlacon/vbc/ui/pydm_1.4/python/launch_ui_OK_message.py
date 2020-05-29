#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from pydm import Display

import json
import sys

class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(parent=parent, args=args, macros=macros)

        # defining macro for PyDMShellCommand (when running "clean_status_PV.py")
        self.Shell_clean_PVs.command = "python ../scripts/clean_status_PV.py " + str(sys.argv[5])

    def ui_filename(self):
        return '../ui/latest/OK_message.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
