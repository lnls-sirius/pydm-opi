#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from qtpy.QtGui import QDesktopServices, QPixmap
from qtpy.QtCore import QUrl

from pydm import Display

from siriushlacon.utils.consts import ARCHIVER_URL, CNPEM_IMG, LNLS_IMG
from siriushlacon.mks937b.consts import PRESSURE, SETTINGS, INFO_UI, \
    DEVICE_MENU_UI


def get_json_macro(macros):
    return json.dumps(macros)


class DeviceMenu(Display):

    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros)
        json_macro = get_json_macro(macros)

        self.btnMON.filenames = [PRESSURE]
        self.btnMON.macros = json_macro

        self.btnSettings.filenames = [SETTINGS]
        self.btnSettings.macros = json_macro

        self.btnInfo.filenames = [INFO_UI]
        self.btnInfo.macros = json_macro

        # self.btnArchiver.clicked.connect(self.open_archiver)

        self.label_cnpem.setPixmap(QPixmap(CNPEM_IMG))
        self.label_lnls.setPixmap(QPixmap(LNLS_IMG))

    def open_archiver(self):
        QDesktopServices.openUrl(QUrl(ARCHIVER_URL))

    def ui_filename(self):
        return DEVICE_MENU_UI

    def ui_filepath(self):
        return DEVICE_MENU_UI
