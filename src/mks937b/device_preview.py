#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydm import Display
from pydm.utilities import IconFont

from src.consts.mks937b import COLD_CATHODE
from src.paths import get_abs_path, DEVICE_PREVIEW_UI, DEVICE_MENU


class DevicePreview(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DevicePreview, self).__init__(
            parent=parent, args=args, macros=macros)
        self.btn1.filenames = [get_abs_path(DEVICE_MENU)]
        self.btn1.setIcon(IconFont().icon('edit'))

        if macros:
            if macros.get('A') == COLD_CATHODE:
                self.PyDMLabel_2.hide()
                self.label_2.hide()

            if macros.get('B') == COLD_CATHODE:
                self.PyDMLabel_4.hide()
                self.label_4.hide()

            if macros.get('C') == COLD_CATHODE:
                self.PyDMLabel_6.hide()
                self.label_6.hide()

    def ui_filename(self):
        return DEVICE_PREVIEW_UI

    def ui_filepath(self):
        return get_abs_path(DEVICE_PREVIEW_UI)
