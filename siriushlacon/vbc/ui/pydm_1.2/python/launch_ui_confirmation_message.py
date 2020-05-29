#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from pydm import Display

import sys

class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(parent=parent, args=args, macros=macros)

        # updating VALVE name
        if (sys.argv[6] == "1"):
            self.VALVE.setText("Pre-vacuum Valve?")
        elif (sys.argv[6] == "2"):
            self.VALVE.setText("Gate Valve?")
        elif (sys.argv[6] == "3"):
            self.VALVE.setText("Valve 3?")
        elif (sys.argv[6] == "4"):
            self.VALVE.setText("Valve 4?")
        elif (sys.argv[6] == "5"):
            self.VALVE.setText("Venting Valve?")

        # select which relay should commute
        self.PyDMShellCommand_no.command = "python ../scripts/commute_valve.py " + str(sys.argv[5]) + " " + sys.argv[6] + " no"
        self.PyDMShellCommand_yes.command = "python ../scripts/commute_valve.py " + str(sys.argv[5]) + " " + sys.argv[6] + " yes"

    def ui_filename(self):
        return '../ui/latest/confirmation_message.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
