#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from os import path
from pydm import Display
from siriushlacon.vbc.consts import OK_MESSAE_UI, CLEAN_STATUS_SCRIPT


class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=OK_MESSAE_UI
        )

        self.Shell_clean_PVs.command = "python {} {}".format(
            CLEAN_STATUS_SCRIPT, sys.argv[5]
        )
