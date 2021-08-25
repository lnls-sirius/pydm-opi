#!/usr/bin/env python3
import sys
import typing as _typing

from pydm import Display
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QWidget as _QWidget

from siriushlacon.utils.command_runner import CommandRunner
from siriushlacon.vbc.consts import CHECK_IMG, OK_MESSAGE_UI, Finished
from siriushlacon.vbc.scripts import clear_status_off, clear_status_on, clear_status_rec
from siriushlacon.widgets.dialog import BaseDialog as _BaseDialog


class OkMessage(Display):
    def __init__(
        self,
        parent=None,
        args=None,
        macros=None,
        prefix: _typing.Optional[str] = None,
        finished: _typing.Optional[_typing.Union[Finished, str]] = None,
    ):
        super(OkMessage, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=OK_MESSAGE_UI
        )
        if not prefix or not finished:
            if len(sys.argv) < 6:
                raise ValueError(f"Invalid arguments {sys.argv}")

            prefix = sys.argv[5]
            finished = sys.argv[6]
            finished = finished.upper().replace(" ", "")
        if not prefix:
            raise ValueError(f"prefix '{prefix}' cannot be empty {self}")
        self.prefix: str = prefix

        self.label_2.setPixmap(QPixmap(CHECK_IMG))
        self.ClearStatusCommand: CommandRunner

        if finished == Finished.ON:
            self.ClearStatusCommand = CommandRunner(
                name=f"ClearStatusOn?prefix={self.prefix}",
                command=lambda: clear_status_on(prefix=self.prefix),
                close_when_finished=True,
                parent_widget=self.parent(),
            )
        elif finished == Finished.OFF:
            self.ClearStatusCommand = CommandRunner(
                name=f"ClearStatusOff?prefix={self.prefix}",
                command=lambda: clear_status_off(prefix=self.prefix),
                close_when_finished=True,
                parent_widget=self.parent(),
            )
        elif finished == Finished.REC:
            self.ClearStatusCommand = CommandRunner(
                name=f"ClearStatusRec?prefix={self.prefix}",
                command=lambda: clear_status_rec(prefix=self.prefix),
                close_when_finished=True,
                parent_widget=self.parent(),
            )
        else:
            raise ValueError(f"Invalid argument {finished}, required {Finished}")

        self.pushButton.clicked.connect(
            lambda *_args, **_kwargs: self.ClearStatusCommand.execute_command()
        )


class OkMessageDialog(_BaseDialog):
    def __init__(
        self,
        parent: _typing.Optional[_QWidget],
        prefix: str,
        finished: Finished,
        macros: _typing.Optional[_typing.Dict[str, str]],
        window_title: str = "VBC - Ok Message",
    ) -> None:
        super().__init__(parent, window_title=window_title, macros=macros)
        display = OkMessage(
            parent=self, macros=macros, finished=finished, prefix=prefix
        )
        self.set_display(display=display)
