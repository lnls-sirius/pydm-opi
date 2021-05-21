#!/usr/bin/env python3

import json
import logging
import subprocess
import typing

from pydm import Display
from qtpy.QtGui import QPixmap

from siriushlacon.utils.command_runner import CommandRunner, ShellCommandRunner
from siriushlacon.utils.consts import CNPEM_IMG, LNLS_IMG
from siriushlacon.vbc.consts import (
    ADVANCED_WINDOW_PY,
    OK_MESSAGE_PY,
    PLAY_IMG,
    SIMPLE_WINDOW_PY,
    STOP_IMG,
    SYSTEM_WINDOW_UI,
    WARNING_WINDOW_PY,
)
from siriushlacon.vbc.scripts import check_pressure, process_off, process_on

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

        # Command Runners
        self.ProcessOnCommand = CommandRunner(
            command=lambda: process_on(self.macros_ioc), name="ProcessOn"
        )
        self.CheckPressureCommand = CommandRunner(
            command=lambda: check_pressure(prefix=self.macros_ioc, first_time=False)
        )
        self.ProcessOffCommand = CommandRunner(
            command=lambda: process_off(prefix=self.macros_ioc)
        )

        # Shell script runners
        self.WarningWindowCommand = ShellCommandRunner(
            command=f"pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {WARNING_WINDOW_PY} {self.macros_ioc}"
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
        self.Shell_ON_button.clicked.connect(
            lambda: self.CheckPressureCommand.execute_command()
        )

        # OFF Button
        self.Shell_OFF_button.clicked.connect(
            lambda: self.ProcessOffCommand.execute_command()
        )
