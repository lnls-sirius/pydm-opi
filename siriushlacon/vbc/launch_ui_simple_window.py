#!/usr/bin/env python3
from qtpy.QtGui import QPixmap
from pydm import Display
from siriushlacon.utils.consts import LNLS_IMG
from siriushlacon.vbc.consts import (
    COMMUTE_VALVE_SCRIPT,
    CONFIRMATION_MESSAGE_PY,
    SIMPLE_WINDOW_UI,
)


class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=SIMPLE_WINDOW_UI
        )
        self.lnlsLabel.setPixmap(QPixmap(LNLS_IMG))
        macros_ioc = macros["IOC"]

        self.Relay1.commands = [f"python {COMMUTE_VALVE_SCRIPT} {macros_ioc} 1 yes"]

        self.Relay1_2.commands = [f"python {COMMUTE_VALVE_SCRIPT} {macros_ioc} 2 yes"]

        self.Relay5.commands = [
            f"pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {CONFIRMATION_MESSAGE_PY} {macros_ioc} 5"
        ]
