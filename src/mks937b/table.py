#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from os import path
from pydm import Display
from pydm.widgets import PyDMRelatedDisplayButton, PyDMEmbeddedDisplay, PyDMLabel

from PyQt5.QtWidgets import QComboBox, QLabel, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt

from src.mks937b.consts import COLD_CATHODE, PIRANI
from src.mks937b.consts import ring_sector_devices, booster_sector_devices, bts_sector_devices, ltb_sector_devices

from src.paths import get_abs_path, TABLE_UI, DEVICE_MENU


class StorageRing(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(StorageRing, self).__init__(
            parent=parent, args=args, macros=macros)

        self.config_table(self.boosterTableWidget, booster_sector_devices)
        self.config_table(self.ringTableWidget, ring_sector_devices)
        self.config_table(self.ltbTableWidget, ltb_sector_devices)
        self.config_table(self.btsTableWidget, bts_sector_devices)

    def add_label(self, table, row, col, pv, *args, **kwargs):
        """
        Add a PYDMLabel to the table.
        """
        table.setCellWidget(row, col, PyDMLabel(table, pv))

    def config_table(self, table, devices):
        """
        Configures a table with the following devices.
        :param table: Parent table.
        :param devices: Devices list according to consts.py.
        """ 
        header_labels = [
            'Device Name',
            'Pressure 1', 'Alarm',
            'Pressure 2', 'Alarm',
            'Pressure 3', 'Alarm',
            'Pressure 4', 'Alarm',
            'Pressure 5', 'Alarm',
            'Pressure 6', 'Alarm',
            'Unit',
            'Device Details']

        table.setRowCount(len(devices))
        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

        for row in range(0, len(devices)):
            # PyDMLabel
            device = devices[row]
            device_name = 'ca://' +  device[4][0]
            table.setCellWidget(row, 0, QLabel(device[4][0]))
            
            self.add_label(table, row, 1, device_name + ':Pressure-Mon-s')
            self.add_label(table, row, 2, device_name + ':Pressure-Mon.STAT') 

            device_name = 'ca://' +  device[4][1]
            self.add_label(table, row, 3, device_name + ':Pressure-Mon-s')
            self.add_label(table, row, 4, device_name + ':Pressure-Mon.STAT') 
            
            device_name = 'ca://' +  device[4][2]
            self.add_label(table, row, 5, device_name + ':Pressure-Mon-s')
            self.add_label(table, row, 6, device_name + ':Pressure-Mon.STAT') 
            
            device_name = 'ca://' +  device[4][3]
            self.add_label(table, row, 7, device_name + ':Pressure-Mon-s')
            self.add_label(table, row, 8, device_name + ':Pressure-Mon.STAT') 
          
            device_name = 'ca://' +  device[4][4]
            self.add_label(table, row, 9, device_name + ':Pressure-Mon-s')
            self.add_label(table, row, 10, device_name + ':Pressure-Mon.STAT') 
           
            device_name = 'ca://' +  device[4][5]
            self.add_label(table, row, 11, device_name + ':Pressure-Mon-s')
            self.add_label(table, row, 12, device_name + ':Pressure-Mon.STAT') 
            
            device_name = 'ca://' +  device[0]
            self.add_label(table, row, 13, device_name + ':Unit', 'Unit') 
            
            rel = PyDMRelatedDisplayButton(table, get_abs_path(DEVICE_MENU))
            rel.openInNewWindow = True
            rel.macros = \
            '{"DEVICE" :"' +  device[0] + '",\
              "G1":"' + device[4][0] + '",\
              "G2":"' + device[4][1] + '",\
              "G3":"' + device[4][2] + '",\
              "G4":"' + device[4][3] + '",\
              "G5":"' + device[4][4] + '",\
              "G6":"' + device[4][5] + '",\
              "A":"' + device[1] + '",\
              "B":"' + device[2] + '", \
              "C":"' + device[3] + '"}'
            table.setCellWidget(row, 14, rel)

    def ui_filename(self):
        return TABLE_UI

    def ui_filepath(self):
        return get_abs_path(TABLE_UI)
