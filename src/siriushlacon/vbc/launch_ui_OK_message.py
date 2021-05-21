#!/usr/bin/env python3
import sys
from qtpy.QtGui import QPixmap
from pydm import Display
from siriushlacon.vbc.consts import OK_MESSAGE_UI, CHECK_IMG
from siriushlacon.vbc.command_runner import CommandRunner
from siriushlacon.vbc.scripts import clean_status_pv


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

        self.CleanStatusCommand = CommandRunner(
            command=lambda: clean_status_pv(prefix=ioc_prefix, finished=finished)
        )

        self.pushButton.clicked(
            lambda *_args, **_kwargs: self.CleanStatusCommand.execute_command()
        )
