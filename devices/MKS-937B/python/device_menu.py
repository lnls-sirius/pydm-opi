#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from pydm import Display
from pydm.widgets import PyDMRelatedDisplayButton

import json

from consts import COLD_CATHODE, PIRANI, ARGS_HIDE_ALL

from macros import get_device_macro


class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        #super(Main, self).__init__(parent=parent, args=args, macros=UI_MACRO_MAIN)
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros)

        self.btnMON.displayFilename = 'pressure.py'
        self.btnMON.macros = json.dumps(get_device_macro(macros.get(
            'DEVICE'), macros.get('A'), macros.get('B'), macros.get('C')))

        self.btnSettings.displayFilename = 'settings.py'
        self.btnSettings.macros = json.dumps(get_device_macro(macros.get(
            'DEVICE'), macros.get('A'), macros.get('B'), macros.get('C')))

        self.btnInfo.displayFilename = '../ui/info.ui'
        self.btnInfo.macros = json.dumps(get_device_macro(macros.get(
            'DEVICE'), macros.get('A'), macros.get('B'), macros.get('C')))

    def ui_filename(self):
        return '../ui/device_menu.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
