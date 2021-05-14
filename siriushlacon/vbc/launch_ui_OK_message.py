#!/usr/bin/env python3
import sys
from qtpy.QtGui import QPixmap
from pydm import Display
from siriushlacon.vbc.consts import OK_MESSAGE_UI, CLEAN_STATUS_SCRIPT, CHECK_IMG
from siriushlacon.vbc.command_runner import ShellCommandRunner


class DeviceMenu(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=OK_MESSAGE_UI
        )
        self.label_2.setPixmap(QPixmap(CHECK_IMG))

        if len(sys.argv) < 6:
            raise RuntimeError(f"Invalid arguments {sys.argv}")

        ioc_prefix = sys.argv[5]
        finished = sys.argv[6]

        self.CleanStatusCommand = ShellCommandRunner(
            command=f"python {CLEAN_STATUS_SCRIPT} {ioc_prefix} {finished}"
        )

        self.pushButton.clicked(
            lambda _, *_args, **_kwargs: self.CleanStatusCommand.execute_command()
        )
