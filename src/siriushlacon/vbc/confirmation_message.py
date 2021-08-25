#!/usr/bin/env python3
import logging as _logging
import sys as _sys
import typing as _typing

from pydm import Display as _Display
from qtpy.QtWidgets import QWidget as _QWidget

from siriushlacon.utils.command_runner import CommandRunner
from siriushlacon.vbc.consts import CONFIRMATION_MESSAGE_UI
from siriushlacon.vbc.images import WARNING as _WARNING_PIXMAP
from siriushlacon.vbc.scripts import commute_valve, set_venting_valve_state
from siriushlacon.widgets.dialog import BaseDialog as _BaseDialog

_logger = _logging.getLogger(__name__)


class ConfirmationMessage(_Display):
    def __init__(
        self,
        parent=None,
        args=None,
        macros=None,
        prefix: _typing.Optional[str] = None,
        relay_number: _typing.Optional[int] = None,
        state: _typing.Optional[bool] = None,
    ):
        super(ConfirmationMessage, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=CONFIRMATION_MESSAGE_UI
        )

        self.label_2.setPixmap(_WARNING_PIXMAP)

        if not prefix or not relay_number:
            if len(_sys.argv) < 6:
                raise ValueError("Missing arguments")

            self.prefix: str = _sys.argv[5]
            self.relay_number: int = int(_sys.argv[6])
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
            name=f"CommuteValve?Relay={self.relay_number},confirmed={True}",
            close_when_finished=True,
            parent_widget=self.parent(),
        )
        self.CommuteValveNoCommand = CommandRunner(
            command=lambda: commute_valve(
                prefix=self.prefix, valve=self.relay_number, confirmed=False
            ),
            name=f"CommuteValve?Relay={self.relay_number},confirmed={False}",
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


class VentingValveConfirmationMessage(_Display):
    def __init__(
        self,
        state: bool,
        prefix: str,
        parent=None,
        args=None,
        macros=None,
    ):
        super(VentingValveConfirmationMessage, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=CONFIRMATION_MESSAGE_UI
        )
        self.label_2.setPixmap(_WARNING_PIXMAP)
        self.prefix = prefix
        self.relay_number = 5
        self.state = state

        text = "(on)" if state else "(off)"
        self.VALVE.setText(f"Venting Valve? {text}")

        self.CommuteValveYesCommand = CommandRunner(
            command=lambda: set_venting_valve_state(prefix=self.prefix, state=state),
            name=f"SetVentingValve?prefix={self.prefix},state={self.state}",
            close_when_finished=True,
            parent_widget=self.parent(),
        )

        self.buttonBox.rejected.connect(self._close)
        self.buttonBox.accepted.connect(
            lambda *_: self.CommuteValveYesCommand.execute_command()
        )

    def _close(self):
        if self.parent() and isinstance(self.parent(), _QWidget):
            self.parent().close()
        else:
            _logger.warning(f"unable to close widget {self}")


class VentingValveConfirmationMessageDialog(_BaseDialog):
    def __init__(
        self,
        parent: _typing.Optional[_QWidget],
        prefix: str,
        state: bool,
        window_title: str = "VBC - Turbo Venting Valve Confirmation Message",
        macros: _typing.Dict[str, str] = None,
    ) -> None:
        super().__init__(parent, window_title=window_title)
        display = VentingValveConfirmationMessage(
            parent=self,
            prefix=prefix,
            macros=macros,
            state=state,
        )
        self.set_display(display=display)
