#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from qtpy.QtGui import QPixmap
from pydm import Display
from siriushlacon.vbc.consts import OK_MESSAGE_UI, CLEAN_STATUS_SCRIPT, CHECK_IMG


class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=OK_MESSAGE_UI
        )
        self.label_2.setPixmap(QPixmap(CHECK_IMG))

        self.Shell_clean_PVs.commands = [
            "python {} {}".format(CLEAN_STATUS_SCRIPT, sys.argv[5])
        ]
