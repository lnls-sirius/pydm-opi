#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydm import Display
from siriushlacon.vbc.consts import (
    WARNING_WINDOW_UI,
    OK_MESSAGE_PY,
    PROCESS_RECOVERYY_SCRIPT,
)

import sys

IOC = str(sys.argv[5])


class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=WARNING_WINDOW_UI
        )

        # defining macro for PyDMShellCommand (for launching "warning_message.ui")
        self.Stage_1.channel = f"ca://{IOC}:ProcessRecovery:Status1"
        self.Stage_2.channel = f"ca://{IOC}:ProcessRecovery:Status2"
        self.Stage_3.channel = f"ca://{IOC}:ProcessRecovery:Status3"
        self.Stage_4.channel = f"ca://{IOC}:ProcessRecovery:Status4"
        self.Stage_5.channel = f"ca://{IOC}:ProcessRecovery:Status5"
        self.pressure_base.channel = f"ca://{IOC}:BBB:TorrBaseMsg"
        self.pressure_exp.channel = f"ca://{IOC}:BBB:TorrExpMsg"

        self.pop_up_OK_message.commands = [
            f"pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {OK_MESSAGE_PY} {IOC}"
        ]
        self.Shell.commands = [f"python {PROCESS_RECOVERYY_SCRIPT} {IOC}"]
