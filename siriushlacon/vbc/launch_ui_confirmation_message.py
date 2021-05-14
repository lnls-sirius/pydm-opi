#!/usr/bin/env python3
import sys
import logging
import subprocess
import typing

from qtpy.QtGui import QPixmap
from pydm import Display
from siriushlacon.vbc.consts import (
    COMMUTE_VALVE_SCRIPT,
    CONFIRMATION_MESSAGE_UI,
    WARNING_IMG,
)

logger = logging.getLogger(__name__)


class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=CONFIRMATION_MESSAGE_UI
        )
        self.CommuteValvePopen: typing.Optional[subprocess.Popen] = None
        self.label_2.setPixmap(QPixmap(WARNING_IMG))

        if len(sys.argv) < 6:
            raise RuntimeError("Missing arguments")

        self.ioc_prefix: str = sys.argv[5]
        self.relay_number: str = sys.argv[6]

        # updating VALVE name
        if self.relay_number == "1":
            self.VALVE.setText("Pre-vacuum Valve?")
        elif self.relay_number == "2":
            self.VALVE.setText("Gate Valve?")
        elif self.relay_number == "3":
            self.VALVE.setText("Valve 3?")
        elif self.relay_number == "4":
            self.VALVE.setText("Valve 4?")
        elif self.relay_number == "5":
            self.VALVE.setText("Venting Valve?")

        self.btnNo.clicked.connect(lambda _: self.CommuteValve(False))
        self.btnYes.clicked.connect(lambda _: self.CommuteValve(True))

    def CommuteValve(self, yes: bool):
        if self.CommuteValvePopen and not self.CommuteValvePopen.poll():
            logger.error(
                f"Commute Valve: Process {self.CommuteValvePopen.pid} still running"
            )
            return

        yes_no = "yes" if yes else "no"
        args = f"python {COMMUTE_VALVE_SCRIPT} {self.ioc_prefix} {self.relay_number} {yes_no}"
        self.CommuteValvePopen = subprocess.Popen(args)
        logger.info(
            f"Commute Valve: Spawn new process with cmd '{args}', PID={self.CommuteValvePopen.pid}"
        )

        # @Fixme!
        exit(0)
