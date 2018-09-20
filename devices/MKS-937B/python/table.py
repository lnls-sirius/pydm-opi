#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from os import path
from pydm import Display
from pydm.widgets import PyDMRelatedDisplayButton, PyDMEmbeddedDisplay, PyDMLabel

from PyQt5.QtWidgets import QComboBox, QLabel, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt
from macros import get_device_macro
from consts import DEVICE_PREFIX, TABLE_UI, COLD_CATHODE, PIRANI, DEVICE_MENU_PY
from consts import ring_sector_devices, booster_sector_devices, bts_sector_devices, ltb_sector_devices

from utils import get_abs_path

class StorageRing(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(StorageRing, self).__init__(
            parent=parent, args=args, macros=macros)
       
        self.config_table(self.boosterTableWidget, booster_sector_devices) 
        self.config_table(self.ringTableWidget, ring_sector_devices) 
        self.config_table(self.ltbTableWidget, ltb_sector_devices) 
        self.config_table(self.btsTableWidget, bts_sector_devices) 

    def get_label(self, parent, content, tooltip):
        lbl = PyDMLabel(parent, content)
        lbl.setToolTip(tooltip)
        return lbl

    def config_table(self, table, devices):
        num_devices = len(devices)
        table.setRowCount(num_devices)
        table.setColumnCount(15)
        table.setHorizontalHeaderLabels(
            ['Device Name',
            'Pressure 1', 'Alarm',
            'Pressure 2', 'Alarm',
            'Pressure 3', 'Alarm',
            'Pressure 4', 'Alarm',
            'Pressure 5', 'Alarm',
            'Pressure 6', 'Alarm',
            'Unit',
            'Device Details'])
        for row in range(0, num_devices):
            # PyDMLabel
            device = devices[row]
            device_name = 'ca://' + DEVICE_PREFIX + device[0]
            table.setCellWidget(row, 0, QLabel(DEVICE_PREFIX + device[0]))
            
            table.setCellWidget(row, 1, self.get_label(table, device_name + ':PressureRb-1s', device[1]))
            table.setCellWidget(row, 2, self.get_label(table, device_name + ':PressureRb-1.STAT', device[1]))
            table.setCellWidget(row, 3, self.get_label(table, device_name + ':PressureRb-2s', device[1]))
            table.setCellWidget(row, 4, ((self.get_label(table, device_name + ':PressureRb-2.STAT', device[1])) if device[1] == PIRANI else QLabel('')))

            table.setCellWidget(row, 5, self.get_label(table, device_name + ':PressureRb-3s', device[2]))
            table.setCellWidget(row, 6, self.get_label(table, device_name + ':PressureRb-3.STAT', device[2]))
            table.setCellWidget(row, 7, self.get_label(table, device_name + ':PressureRb-4s', device[2]))
            table.setCellWidget(row, 4, ((self.get_label(table, device_name + ':PressureRb-4.STAT', device[2])) if device[2] == PIRANI else QLabel('')))
            
            table.setCellWidget(row, 9, self.get_label(table, device_name + ':PressureRb-5s', device[3]))
            table.setCellWidget(row, 10, self.get_label(table, device_name + ':PressureRb-5.STAT', device[3]))
            table.setCellWidget(row, 11, self.get_label(table, device_name + ':PressureRb-6s', device[3]))
            table.setCellWidget(row, 12, ((self.get_label(table, device_name + ':PressureRb-6.STAT', device[3])) if device[3] == PIRANI else QLabel('')))
            
            table.setCellWidget(row, 13, self.get_label(table, device_name + ':Unit', 'Unit'))
            
            rel = PyDMRelatedDisplayButton(table, get_abs_path(DEVICE_MENU_PY))
            rel.openInNewWindow = True
            rel.macros = '{"DEVICE" :"' + DEVICE_PREFIX + device[0] +'", "A":"' + device[1] + '","B":"'+device[2]+'", "C":"'+device[3]+'"}'
            table.setCellWidget(row, 14, rel)

    def ui_filename(self):
        return TABLE_UI

    def ui_filepath(self):
        return get_abs_path(TABLE_UI)
 