#!/usr/bin/env python3
import sys

from pydm import Display
from qtpy.QtGui import QPixmap

from siriushlacon.utils.command_runner import CommandRunner
from siriushlacon.vbc.consts import CHECK_IMG, OK_MESSAGE_UI, Finished
from siriushlacon.vbc.scripts import clear_status_off, clear_status_on, clear_status_rec


class DeviceMenu(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=OK_MESSAGE_UI
        )
        self.label_2.setPixmap(QPixmap(CHECK_IMG))

        if len(sys.argv) < 6:
            raise ValueError(f"Invalid arguments {sys.argv}")

        ioc_prefix = sys.argv[5]
        finished = sys.argv[6]

        self.ClearStatusCommand: CommandRunner

        finished = finished.upper().replace(" ", "")
        if finished == Finished.ON.value:
            self.ClearStatusCommand: CommandRunner = CommandRunner(
                command=lambda: clear_status_on(prefix=ioc_prefix)
            )
        elif finished == Finished.OFF.value:
            self.ClearStatusCommand: CommandRunner = CommandRunner(
                command=lambda: clear_status_off(prefix=ioc_prefix)
            )
        elif finished == Finished.REC.value:
            self.ClearStatusCommand: CommandRunner = CommandRunner(
                command=lambda: clear_status_rec(prefix=ioc_prefix)
            )
        else:
            raise ValueError(f"Invalid argument {finished}, required {Finished}")

        self.pushButton.clicked.connect(
            lambda *_args, **_kwargs: self.ClearStatusCommand.execute_command()
        )
