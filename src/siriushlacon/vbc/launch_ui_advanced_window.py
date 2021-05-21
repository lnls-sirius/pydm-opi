#!/usr/bin/env python3

from pydm import Display
from qtpy.QtGui import QPixmap

from siriushlacon.utils.command_runner import ShellCommandRunner
from siriushlacon.utils.consts import CNPEM_IMG, LNLS_IMG
from siriushlacon.vbc.consts import ADVANCED_WINDOW_UI, CONFIRMATION_MESSAGE_PY


class DeviceMenu(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=ADVANCED_WINDOW_UI
        )

        self.lnlsLabel.setPixmap(QPixmap(LNLS_IMG))
        self.cnpemLabel.setPixmap(QPixmap(CNPEM_IMG))
        # defining macros for PyDMShellCommand (valve open/close confirmation)
        macros_ioc = macros["IOC"]
        RELAY_SH_STR = f"pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {CONFIRMATION_MESSAGE_PY} {macros_ioc}"

        self.Relay1ConfirmationCommand = ShellCommandRunner(command=f"{RELAY_SH_STR} 1")
        self.Relay2ConfirmationCommand = ShellCommandRunner(command=f"{RELAY_SH_STR} 2")
        self.Relay3ConfirmationCommand = ShellCommandRunner(command=f"{RELAY_SH_STR} 3")
        self.Relay4ConfirmationCommand = ShellCommandRunner(command=f"{RELAY_SH_STR} 4")
        self.Relay5ConfirmationCommand = ShellCommandRunner(command=f"{RELAY_SH_STR} 5")

        self.PyDMCheckbox_Relay1.clicked.connect(
            lambda *_args: self.Relay1ConfirmationCommand.execute_command()
        )
        self.PyDMCheckbox_Relay2.clicked.connect(
            lambda *_args: self.Relay2ConfirmationCommand.execute_command()
        )
        self.PyDMCheckbox_Relay3.clicked.connect(
            lambda *_args: self.Relay3ConfirmationCommand.execute_command()
        )
        self.PyDMCheckbox_Relay4.clicked.connect(
            lambda *_args: self.Relay4ConfirmationCommand.execute_command()
        )
        self.PyDMCheckbox_Relay5.clicked.connect(
            lambda *_args: self.Relay5ConfirmationCommand.execute_command()
        )
