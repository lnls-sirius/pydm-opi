#!/usr/bin/env python3

import json
import typing
import subprocess
import logging

from qtpy.QtGui import QPixmap
from pydm import Display

from siriushlacon.vbc.consts import (
    ADVANCED_WINDOW_PY,
    CHECK_PRESSURE_SCRIPT,
    OK_MESSAGE_PY,
    PLAY_IMG,
    PROCESS_OFF_SCRIPT,
    PROCESS_ON_SCRIPT,
    SIMPLE_WINDOW_PY,
    STOP_IMG,
    SYSTEM_WINDOW_UI,
    WARNING_WINDOW_PY,
)
from siriushlacon.vbc.command_runner import ShellCommandRunner
from siriushlacon.utils.consts import LNLS_IMG, CNPEM_IMG


logger = logging.getLogger(__name__)


class DeviceMenu(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=SYSTEM_WINDOW_UI
        )
        self.lblOn.setPixmap(QPixmap(PLAY_IMG))
        self.lblOff.setPixmap(QPixmap(STOP_IMG))

        self.lnlsLabel.setPixmap(QPixmap(LNLS_IMG))
        self.cnpemLabel.setPixmap(QPixmap(CNPEM_IMG))

        self.WarningMessagePopen: typing.Optional[subprocess.Popen] = None

        self.macros_ioc = macros["IOC"]

        # Shell script runners
        self.WarningWindowCommand = ShellCommandRunner(
            command=f"pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {WARNING_WINDOW_PY} {self.macros_ioc}"
        )
        self.ProcessOnCommand = ShellCommandRunner(
            command=f"python {PROCESS_ON_SCRIPT} {self.macros_ioc}"
        )
        self.LaunchOkMessageOnCommand = ShellCommandRunner(
            command=f"pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {OK_MESSAGE_PY} {self.macros_ioc} ON"
        )
        self.LaunchOkMessageOffCommand = ShellCommandRunner(
            command=f"pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {OK_MESSAGE_PY} {self.macros_ioc} OFF"
        )

        # Trigger (usually by an external script)
        self.Shell_PV_trigger_PRESSURIZED.toggled.connect(
            lambda *_args, **_kwargs: self.WarningWindowCommand.execute_command()
        )
        self.Shell_PV_trigger_ON.toggled.connect(
            lambda *_args, **_kwargs: self.ProcessOnCommand.execute_command()
        )
        self.Shell_PV_Trigger_OK_MESSAGE_ON.toggled.connect(
            lambda *_args, **_kwargs: self.LaunchOkMessageOnCommand.execute_command()
        )
        self.Shell_PV_Trigger_OK_MESSAGE_OFF.toggled.connect(
            lambda *_args, **_kwargs: self.LaunchOkMessageOffCommand.execute_command()
        )

        self.btnSimpleTab.macros = json.dumps({"IOC": self.macros_ioc})
        self.btnSimpleTab.filenames = [SIMPLE_WINDOW_PY]

        self.btnAdvancedTab.macros = json.dumps({"IOC": self.macros_ioc})
        self.btnAdvancedTab.filenames = [ADVANCED_WINDOW_PY]

        # ON Button
        self.Shell_ON_button.commands = [
            f"python {CHECK_PRESSURE_SCRIPT} {self.macros_ioc} 0"
        ]

        # OFF Button
        self.Shell_OFF_button.commands = [
            f"python {PROCESS_OFF_SCRIPT} {self.macros_ioc}"
        ]
