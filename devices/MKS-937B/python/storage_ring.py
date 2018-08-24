#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
from pydm import Display
from pydm.widgets import related_display_button, PyDMEmbeddedDisplay

import json

from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSlot,Qt

from macros import get_device_macro 

from consts import DEVICE_PREFIX, STORAGE_RING_UI, NONE_UI, DEVICE_PREVIEW_PY
from consts import ring_sub_sectors as sub_sectors, ring_sector_devices as sector_devices

from utils import get_abs_path


def get_dev_str(num, modfier):
    return json.dumps(get_device_macro(
        device='{}{}'.format(DEVICE_PREFIX, sector_devices[num + modfier][0]),
        a=sector_devices[num + modfier][1],
        b=sector_devices[num + modfier][2],
        c=sector_devices[num + modfier][3]
    ))

class StorageRing(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(StorageRing, self).__init__(parent=parent, args=args, macros=macros) 

        self.cb_sector.addItems(sub_sectors)
        self.cb_sector.setEnabled(True)

        self.cb_sector.currentIndexChanged.connect(self.change_sub_sector)
        self.cb_sector.currentTextChanged.connect(self.title_update)

        self.title_update('1')
        self.change_sub_sector(0)


    def ui_filename(self):
        return STORAGE_RING_UI

    def ui_filepath(self):
        return get_abs_path(STORAGE_RING_UI)

    def change_display(self, display, macros):
        if display: 
            display.disconnect() 
            if display.embedded_widget:
                display.embedded_widget.setAttribute(Qt.WA_DeleteOnClose, True)
                display.embedded_widget.close()
                display.embedded_widget.deleteLater()
            
            display.macros = macros
            display.filename = get_abs_path(NONE_UI)
            display.filename = get_abs_path(DEVICE_PREVIEW_PY)
            

    @pyqtSlot(int)
    def change_sub_sector(self, index):
        sub_sector_modfier = index * 6

        self.change_display(self.disp_1, get_dev_str(0, sub_sector_modfier))
        self.change_display(self.disp_2, get_dev_str(1, sub_sector_modfier))
        self.change_display(self.disp_3, get_dev_str(2, sub_sector_modfier))
        self.change_display(self.disp_4, get_dev_str(3, sub_sector_modfier))
        self.change_display(self.disp_5, get_dev_str(4, sub_sector_modfier))
        self.change_display(self.disp_6, get_dev_str(5, sub_sector_modfier))

            
    @pyqtSlot(str)
    def title_update(self, sub_sector):
        self.lbl_title.setText("Storage Ring\t{}".format(sub_sector))

 