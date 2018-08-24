#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from pydm import Display
from pydm.widgets import PyDMRelatedDisplayButton

import json

from consts import COLD_CATHODE, PIRANI, ARGS_HIDE_ALL, PRESSURE_PY, SETTINGS_PY, SETTINGS_UI, \
    INFO_UI, PRESSURE_PY, DEVICE_MENU_UI

from utils import get_abs_path

from macros import get_device_macro


class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(parent=parent, args=args, macros=macros)

        self.btnMON.displayFilename = get_abs_path(PRESSURE_PY)     
        self.btnMON.macros = json.dumps(get_device_macro(macros.get(
            'DEVICE'), macros.get('A'), macros.get('B'), macros.get('C')))

        self.btnSettings.displayFilename = get_abs_path(SETTINGS_PY)
        self.btnSettings.macros = json.dumps(get_device_macro(macros.get(
            'DEVICE'), macros.get('A'), macros.get('B'), macros.get('C')))

        self.btnInfo.displayFilename = get_abs_path(INFO_UI)
        self.btnInfo.macros = json.dumps(get_device_macro(macros.get(
            'DEVICE'), macros.get('A'), macros.get('B'), macros.get('C')))

    def ui_filename(self):
        return DEVICE_MENU_UI

    def ui_filepath(self):
        return get_abs_path(DEVICE_MENU_UI)
