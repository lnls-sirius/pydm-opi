#!/usr/bin/env python3

import json
import logging
import subprocess
import typing

from pydm import Display
from qtpy.QtGui import QPixmap

from siriushlacon.utils.command_runner import CommandRunner
from siriushlacon.vbc.consts import (
    ADVANCED_WINDOW_PY,
    PLAY_IMG,
    SIMPLE_WINDOW_PY,
    STOP_IMG,
    SYSTEM_WINDOW_UI,
    Finished,
)
from siriushlacon.vbc.OK_message import OkMessageDialog
from siriushlacon.vbc.scripts import check_pressure, process_off, process_on
from siriushlacon.vbc.warning_message import (
    VBCWarningMessageDialog as _VBCWarningMessageDialog,
)
from siriushlacon.widgets.images import CNPEM_PIXMAP, LNLS_PIXMAP

logger = logging.getLogger(__name__)


class DeviceMenu(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=SYSTEM_WINDOW_UI
        )
        self.lblOn.setPixmap(QPixmap(PLAY_IMG))
        self.lblOff.setPixmap(QPixmap(STOP_IMG))

        self.lnlsLabel.setPixmap(LNLS_PIXMAP)
        self.lnlsLabel.setFixedSize(LNLS_PIXMAP.size())

        self.cnpemLabel.setPixmap(CNPEM_PIXMAP)
        self.cnpemLabel.setFixedSize(CNPEM_PIXMAP.size())

        self.WarningMessagePopen: typing.Optional[subprocess.Popen] = None

        self.prefix = macros["IOC"]

        # Command Runners
        self.ProcessOnCommand = CommandRunner(
            command=lambda: process_on(self.prefix), name="ProcessOn"
        )
        self.CheckPressureCommand = CommandRunner(
            command=lambda: check_pressure(prefix=self.prefix, first_time=False)
        )
        self.ProcessOffCommand = CommandRunner(
            command=lambda: process_off(prefix=self.prefix)
        )

        # Trigger (usually by an external script)
        self.Shell_PV_trigger_PRESSURIZED.toggled.connect(self.display_warning_message)
        self.Shell_PV_trigger_ON.toggled.connect(
            lambda *_args, **_kwargs: self.ProcessOnCommand.execute_command()
        )
        self.Shell_PV_Trigger_OK_MESSAGE_ON.toggled.connect(self._display_on_message)
        self.Shell_PV_Trigger_OK_MESSAGE_OFF.toggled.connect(self._display_off_message)

        self.btnSimpleTab.macros = json.dumps({"IOC": self.prefix})
        self.btnSimpleTab.filenames = [SIMPLE_WINDOW_PY]

        self.btnAdvancedTab.macros = json.dumps({"IOC": self.prefix})
        self.btnAdvancedTab.filenames = [ADVANCED_WINDOW_PY]

        # ON Button
        self.Shell_ON_button.clicked.connect(
            lambda: self.CheckPressureCommand.execute_command()
        )

        # OFF Button
        self.Shell_OFF_button.clicked.connect(
            lambda: self.ProcessOffCommand.execute_command()
        )

    def _display_ok_message(self, finished: Finished, *_):
        dialog = OkMessageDialog(
            parent=self, finished=finished, prefix=self.prefix, macros=self.macros()
        )
        dialog.show()

    def _display_on_message(self, *_):
        self._display_ok_message(finished=Finished.ON)

    def _display_off_message(self, *_):
        self._display_ok_message(finished=Finished.OFF)

    def display_warning_message(self):
        dialog = _VBCWarningMessageDialog(
            parent=self, prefix=self.prefix, macros=self.macros()
        )
        dialog.show()
