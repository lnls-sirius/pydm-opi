#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
import json

from pydm import Display
from pydm.widgets import PyDMRelatedDisplayButton
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl


from src.paths import get_abs_path, PRESSURE, SETTINGS, SETTINGS_UI, \
    INFO_UI, PRESSURE, DEVICE_MENU_UI

from src.consts import ARCHIVER_URL, ARGS_HIDE_ALL
from src.consts.mks937b import COLD_CATHODE, PIRANI
from src.mks937b.macros import get_device_macro

def get_json_macro(macros):
    return json.dumps(macros)
    
class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros)
        json_macro = get_json_macro(macros)

        self.btnMON.displayFilename = get_abs_path(PRESSURE)
        self.btnMON.macros = json_macro

        self.btnSettings.displayFilename = get_abs_path(SETTINGS)
        self.btnSettings.macros = json_macro

        self.btnInfo.displayFilename = get_abs_path(INFO_UI)
        self.btnInfo.macros = json_macro

        self.btnArchiver.clicked.connect(self.open_archiver)

    def open_archiver(self):
        QDesktopServices.openUrl(QUrl(ARCHIVER_URL))

    def ui_filename(self):
        return DEVICE_MENU_UI

    def ui_filepath(self):
        return get_abs_path(DEVICE_MENU_UI)
