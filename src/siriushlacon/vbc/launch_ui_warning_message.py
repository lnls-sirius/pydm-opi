#!/usr/bin/env python3
import sys
from pydm import Display
from qtpy.QtGui import QPixmap

from siriushlacon.vbc.consts import (
    WARNING_WINDOW_UI,
    OK_MESSAGE_PY,
    PROCESS_RECOVERY_SCRIPT,
)
from siriushlacon.vbc.command_runner import ShellCommandRunner
from siriushlacon.utils.consts import CNPEM_IMG


IOC = str(sys.argv[5])


class DeviceMenu(Display):
    def __init__(self, parent=None, args=None, macros=None):
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

        self.label_9.setPixmap(QPixmap(CNPEM_IMG))

        self.ProcessRecoveryCommand = ShellCommandRunner(
            command=f"python {PROCESS_RECOVERY_SCRIPT} {IOC}"
        )
        self.OkMessageCommand = ShellCommandRunner(
            command=f"pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {OK_MESSAGE_PY} {IOC} REC"
        )

        self.Shell_PV_Trigger_OK_MESSAGE.toggled.connect(
            lambda *_args, **_kwargs: self.OkMessageCommand.execute_command()
        )
        self.buttonBox_2.accepted.connect(
            lambda *_args, **_kwargs: self.ProcessRecoveryCommand.execute_command()
        )
