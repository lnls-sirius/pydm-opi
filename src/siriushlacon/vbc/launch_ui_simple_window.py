#!/usr/bin/env python3
import logging

from pydm import Display
from qtpy.QtGui import QPixmap

from siriushlacon.utils.command_runner import CommandRunner, ShellCommandRunner
from siriushlacon.utils.consts import LNLS_IMG
from siriushlacon.vbc.consts import CONFIRMATION_MESSAGE_PY, SIMPLE_WINDOW_UI
from siriushlacon.vbc.scripts import commute_valve

logger = logging.getLogger(__name__)


class DeviceMenu(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=SIMPLE_WINDOW_UI
        )
        self.lnlsLabel.setPixmap(QPixmap(LNLS_IMG))
        self.macros_ioc: str = macros["IOC"]

        self.CommuteValve1Command = CommandRunner(
            command=lambda: commute_valve(
                prefix=self.macros_ioc, valve=1, confirmed=True
            ),
            name="CommuteValve1_True",
        )

        self.CommuteValve2Command = CommandRunner(
            command=lambda: commute_valve(
                prefix=self.macros_ioc, valve=2, confirmed=True
            ),
            name="CommuteValve2_True",
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
