#!/usr/bin/env python3
import logging

from qtpy.QtGui import QPixmap
from pydm import Display

from siriushlacon.utils.consts import LNLS_IMG
from siriushlacon.vbc.command_runner import ShellCommandRunner
from siriushlacon.vbc.consts import (
    COMMUTE_VALVE_SCRIPT,
    CONFIRMATION_MESSAGE_PY,
    SIMPLE_WINDOW_UI,
)

logger = logging.getLogger(__name__)


class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=SIMPLE_WINDOW_UI
        )
        self.lnlsLabel.setPixmap(QPixmap(LNLS_IMG))
        self.macros_ioc: str = macros["IOC"]

        self.CommuteValve1Command = ShellCommandRunner(
            command=f"python {COMMUTE_VALVE_SCRIPT} {self.macros_ioc} 1 yes"
        )
        self.CommuteValve2Command = ShellCommandRunner(
            command=f"python {COMMUTE_VALVE_SCRIPT} {self.macros_ioc} 2 yes"
        )
        self.ConfirmationMessageCommand = ShellCommandRunner(
            command=f"pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {CONFIRMATION_MESSAGE_PY} {self.macros_ioc} 5"
        )

        self.ChkBoxPreVacValve.clicked.connect(
            lambda *args, **kwargs: self.CommuteValve1Command.execute_command()
        )
        self.ChkGateValve.clicked.connect(
            lambda *args, **kwargs: self.CommuteValve2Command.execute_command()
        )
        self.ChkTurboVentingValve.clicked.connect(
            lambda *_args, **_kwargs: self.ConfirmationMessageCommand.execute_command()
        )
