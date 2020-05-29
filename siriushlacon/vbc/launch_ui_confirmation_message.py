#!/usr/bin/env python3
import sys
from pydm import Display
from siriushlacon.vbc.consts import CONFIRMATION_MESSAGE, COMMUTE_VALVE_SCRIPT


class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=CONFIRMATION_MESSAGE
        )

        # updating VALVE name
        if sys.argv[6] == "1":
            self.VALVE.setText("Pre-vacuum Valve?")
        elif sys.argv[6] == "2":
            self.VALVE.setText("Gate Valve?")
        elif sys.argv[6] == "3":
            self.VALVE.setText("Valve 3?")
        elif sys.argv[6] == "4":
            self.VALVE.setText("Valve 4?")
        elif sys.argv[6] == "5":
            self.VALVE.setText("Venting Valve?")

        # select which relay should commute
        self.PyDMShellCommand_no.command = "python {} {} {} no".format(
            COMMUTE_VALVE_SCRIPT, sys.argv[5], sys.argv[6]
        )
        self.PyDMShellCommand_yes.command = "python {} {} {} yes".format(
            COMMUTE_VALVE_SCRIPT, sys.argv[5], sys.argv[6]
        )
