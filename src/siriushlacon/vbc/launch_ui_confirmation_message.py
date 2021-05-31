#!/usr/bin/env python3
import logging
import subprocess
import sys
import typing

from pydm import Display
from qtpy.QtGui import QPixmap

from siriushlacon.utils.command_runner import CommandRunner
from siriushlacon.vbc.consts import CONFIRMATION_MESSAGE_UI, WARNING_IMG
from siriushlacon.vbc.scripts import commute_valve

logger = logging.getLogger(__name__)


class DeviceMenu(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=CONFIRMATION_MESSAGE_UI
        )
        self.CommuteValvePopen: typing.Optional[subprocess.Popen] = None
        self.label_2.setPixmap(QPixmap(WARNING_IMG))

        if len(sys.argv) < 6:
            raise RuntimeError("Missing arguments")

        self.ioc_prefix: str = sys.argv[5]
        self.relay_number: int = int(sys.argv[6])

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
                prefix=self.ioc_prefix, valve=self.relay_number, confirmed=True
            ),
            name=f"CommuteValveYes_Relay{self.relay_number}",
        )
        self.CommuteValveNoCommand = CommandRunner(
            command=lambda: commute_valve(
                prefix=self.ioc_prefix, valve=self.relay_number, confirmed=False
            ),
            name=f"CommuteValveNo_Relay{self.relay_number}",
        )

        self.buttonBox.rejected.connect(
            lambda *_args, **_kwargs: self.CommuteValveNoCommand.execute_command()
        )
        self.buttonBox.accepted.connect(
            lambda *_args, **_kwargs: self.CommuteValveYesCommand.execute_command()
        )
