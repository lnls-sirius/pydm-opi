#!/usr/bin/env python3
import logging

from pydm import Display

from siriushlacon.utils.command_runner import CommandRunner
from siriushlacon.vbc.confirmation_message import VentingValveConfirmationMessageDialog
from siriushlacon.vbc.consts import SIMPLE_WINDOW_UI
from siriushlacon.vbc.scripts import commute_valve
from siriushlacon.widgets.images import LNLS_PIXMAP

logger = logging.getLogger(__name__)


class DeviceMenu(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=SIMPLE_WINDOW_UI
        )
        self.lnlsLabel.setPixmap(LNLS_PIXMAP)
        self.lnlsLabel.setFixedSize(LNLS_PIXMAP.size())

        self.prefix: str = macros["IOC"]

        self.CommuteValve1Command = CommandRunner(
            command=lambda: commute_valve(prefix=self.prefix, valve=1, confirmed=True),
            name="CommuteValve1_True",
        )

        self.CommuteValve2Command = CommandRunner(
            command=lambda: commute_valve(prefix=self.prefix, valve=2, confirmed=True),
            name="CommuteValve2_True",
        )

        self.ChkBoxPreVacValve.clicked.connect(
            lambda *_args, **_kwargs: self.CommuteValve1Command.execute_command()
        )
        self.ChkGateValve.clicked.connect(
            lambda *_args, **_kwargs: self.CommuteValve2Command.execute_command()
        )

        self.btn_on_turbo_vent_valve.clicked.connect(
            lambda *_args: self.show_confirmation_message(True)
        )
        self.btn_off_turbo_vent_valve.clicked.connect(
            lambda *_args: self.show_confirmation_message(False)
        )

    def show_confirmation_message(self, state: bool):
        dialog = VentingValveConfirmationMessageDialog(self, self.prefix, state)
        dialog.show()
