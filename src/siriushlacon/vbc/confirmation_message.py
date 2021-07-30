#!/usr/bin/env python3
import logging
import sys
import typing as _typing

from pydm import Display
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QWidget as _QWidget

from siriushlacon.utils.command_runner import CommandRunner
from siriushlacon.utils.dialog import BaseDialog as _BaseDialog
from siriushlacon.vbc.consts import CONFIRMATION_MESSAGE_UI, WARNING_IMG
from siriushlacon.vbc.scripts import commute_valve

_logger = logging.getLogger(__name__)


class ConfirmationMessage(Display):
    def __init__(
        self,
        parent=None,
        args=None,
        macros=None,
        prefix: _typing.Optional[str] = None,
        relay_number: _typing.Optional[int] = None,
    ):
        super(ConfirmationMessage, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=CONFIRMATION_MESSAGE_UI
        )

        self.label_2.setPixmap(QPixmap(WARNING_IMG))

        if not prefix or not relay_number:
            if len(sys.argv) < 6:
                raise ValueError("Missing arguments")

            self.prefix: str = sys.argv[5]
            self.relay_number: int = int(sys.argv[6])
        else:
            self.relay_number = relay_number
            self.prefix = prefix

        # updating VALVE name
        if self.relay_number == 1:
            self.VALVE.setText("Pre-vacuum Valve?")
        elif self.relay_number == 2:
            self.VALVE.setText("Gate Valve?")
        elif self.relay_number == 3:
            self.VALVE.setText("Valve 3?")
        elif self.relay_number == 4:
            self.VALVE.setText("Valve 4?")
        elif self.relay_number == 5:
            self.VALVE.setText("Venting Valve?")

        self.CommuteValveYesCommand = CommandRunner(
            command=lambda: commute_valve(
                prefix=self.prefix, valve=self.relay_number, confirmed=True
            ),
            name=f"CommuteValveYes_Relay{self.relay_number}",
            close_when_finished=True,
            parent_widget=self.parent(),
        )
        self.CommuteValveNoCommand = CommandRunner(
            command=lambda: commute_valve(
                prefix=self.prefix, valve=self.relay_number, confirmed=False
            ),
            name=f"CommuteValveNo_Relay{self.relay_number}",
            close_when_finished=True,
            parent_widget=self.parent(),
        )

        self.buttonBox.rejected.connect(
            lambda *_: self.CommuteValveNoCommand.execute_command()
        )
        self.buttonBox.accepted.connect(
            lambda *_: self.CommuteValveYesCommand.execute_command()
        )


class ConfirmationMessageDialog(_BaseDialog):
    def __init__(
        self,
        parent: _typing.Optional[_QWidget],
        prefix: str,
        relay_number: int,
        window_title: str = "VBC - Confirmation Message",
        macros: _typing.Dict[str, str] = None,
    ) -> None:
        super().__init__(parent, window_title=window_title)
        display = ConfirmationMessage(
            parent=self, prefix=prefix, relay_number=relay_number, macros=macros
        )
        self.set_display(display=display)
