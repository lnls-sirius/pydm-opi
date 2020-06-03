#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from qtpy.QtGui import QPixmap
from pydm import Display
from siriushlacon.utils.consts import LNLS_IMG
from siriushlacon.vbc.consts import (
    SIMPLE_WINDOW_UI,
    COMMUTE_VALVE_SCRIPT,
    CONFIRMATION_MESSAGE_PY,
)

import json


class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=SIMPLE_WINDOW_UI
        )
        self.lnlsLabel.setPixmap(QPixmap(LNLS_IMG))
        # self.Relay1.commands = [
        #    "python {} {} 1 yes".format(COMMUTE_VALVE_SCRIPT, macros["IOC"])
        # ]
        # self.Relay5.commands = [
        #    "pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {} {} 5".format(
        #        CONFIRMATION_MESSAGE_PY, macros["IOC"]
        #    )
        # ]
        # self.Relay1_2.commands = [
        #    "python {} {} 2 yes".format(COMMUTE_VALVE_SCRIPT, macros["IOC"])
        # ]
