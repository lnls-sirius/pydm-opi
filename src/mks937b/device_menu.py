#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from qtpy.QtGui import QDesktopServices
from qtpy.QtCore import QUrl

from pydm import Display

from src.paths import get_abs_path, PRESSURE, SETTINGS, \
    INFO_UI, DEVICE_MENU_UI

from src.consts import ARCHIVER_URL


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

        # self.btnArchiver.clicked.connect(self.open_archiver)

    def open_archiver(self):
        QDesktopServices.openUrl(QUrl(ARCHIVER_URL))

    def ui_filename(self):
        return DEVICE_MENU_UI

    def ui_filepath(self):
        return get_abs_path(DEVICE_MENU_UI)
