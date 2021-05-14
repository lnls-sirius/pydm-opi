#!/usr/bin/env python3
# import logging
# import subprocess
import sys

# import typing
# import inspect

from pydm import Display
from qtpy.QtGui import QPixmap

from siriushlacon.vbc.consts import (
    WARNING_WINDOW_UI,
    OK_MESSAGE_PY,
    PROCESS_RECOVERY_SCRIPT,
)
from siriushlacon.utils.consts import CNPEM_IMG

# logger = logging.getLogger(__name__)

IOC = str(sys.argv[5])


class DeviceMenu(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=WARNING_WINDOW_UI
        )

        # defining macro for PyDMShellCommand (for launching "warning_message.ui")
        self.Stage_1.channel = f"ca://{IOC}:ProcessRecovery:Status1"
        self.Stage_2.channel = f"ca://{IOC}:ProcessRecovery:Status2"
        self.Stage_3.channel = f"ca://{IOC}:ProcessRecovery:Status3"
        self.Stage_4.channel = f"ca://{IOC}:ProcessRecovery:Status4"
        self.Stage_5.channel = f"ca://{IOC}:ProcessRecovery:Status5"
        self.pressure_base.channel = f"ca://{IOC}:BBB:TorrBaseMsg"
        self.pressure_exp.channel = f"ca://{IOC}:BBB:TorrExpMsg"

        self.label_9.setPixmap(QPixmap(CNPEM_IMG))

        # self.OkMessagePopen: typing.Optional[subprocess.Popen] = None
        # self.ProcessRecoveryPopen: typing.Optional[subprocess.Popen] = None

        # self.Shell_PV_Trigger_OK_MESSAGE.toggled.connect(self.LaunchOkMessage)
        # self.buttonBox_2.accepted.connect(self.LaunchProcessRecovery)

        self.Shell_OK_MESSAGE.commands = [
            f"pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {OK_MESSAGE_PY} {IOC}"
        ]
        self.Shell_rec_script.commands = [f"python {PROCESS_RECOVERY_SCRIPT} {IOC}"]


#   def LaunchProcessRecovery(self, *args, **kwargs):
#       fname = inspect.currentframe().f_code.co_name
#       if self.ProcessRecoveryPopen and not self.ProcessRecoveryPopen.poll():
#           logger.error(
#               f"{fname}: Process {self.ProcessRecoveryPopen.pid} still running"
#           )
#           return

#       args = f"python {PROCESS_RECOVERY_SCRIPT} {IOC}"
#       self.ProcessRecoveryPopen = subprocess.Popen(args)
#       logger.info(
#           f"{fname}: Spawn new process with cmd '{args}', PID={self.ProcessRecoveryPopen.pid}"
#       )

#   def LaunchOkMessage(self, *args, **kwargs):
#       fname = inspect.currentframe().f_code.co_name
#       if self.OkMessagePopen and not self.OkMessagePopen.poll():
#           logger.error(f"{fname}: Process {self.OkMessagePopen.pid} still running")
#           return

#       args = f"pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {OK_MESSAGE_PY} {IOC}"
#       self.OkMessagePopen = subprocess.Popen(args)
#       logger.info(
#           f"{fname}: Spawn new process with cmd '{args}', PID={self.OkMessagePopen.pid}"
#       )
