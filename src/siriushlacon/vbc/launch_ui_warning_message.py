#!/usr/bin/env python3
import sys

from pydm import Display
from qtpy.QtGui import QPixmap

from siriushlacon.utils.command_runner import CommandRunner, ShellCommandRunner
from siriushlacon.utils.consts import CNPEM_IMG
from siriushlacon.vbc.consts import OK_MESSAGE_PY, WARNING_WINDOW_UI
from siriushlacon.vbc.scripts import process_recovery

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

        self.ProcessRecoveryCommand = CommandRunner(
            command=lambda: process_recovery(IOC), name="ProcessRecovery"
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
