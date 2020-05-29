#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from pydm import Display

import sys
IOC = str(sys.argv[5])

class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(parent=parent, args=args, macros=macros)

        # defining macro for PyDMShellCommand (for launching "warning_message.ui")
        self.Stage_1.channel = "ca://" + IOC + ":ProcessRecovery:Status1"
        self.Stage_2.channel = "ca://" + IOC + ":ProcessRecovery:Status2"
        self.Stage_3.channel = "ca://" + IOC + ":ProcessRecovery:Status3"
        self.Stage_4.channel = "ca://" + IOC + ":ProcessRecovery:Status4"
        self.Stage_5.channel = "ca://" + IOC + ":ProcessRecovery:Status5"
        self.pressure_base.channel = "ca://" + IOC + ":BBB:TorrBaseMsg"
        self.pressure_exp.channel = "ca://" + IOC + ":BBB:TorrExpMsg"

    def ui_filename(self):
        return '../ui/latest/warning_message.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
