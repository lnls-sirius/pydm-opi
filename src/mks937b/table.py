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

    def get_label(self,parent, *args, **kwargs):
        lbl = PyDMLabel(parent, args[0])
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
            
            device_name = 'ca://' +  device[4][0]
            table.setCellWidget(row, 0, QLabel(device[4][0]))
            table.setCellWidget(row, 1, self.get_label(
                table, device_name + ':Pressure-RB-s'))
            table.setCellWidget(row, 2, self.get_label(
                table, device_name + ':Pressure-RB.STAT'))

            device_name = 'ca://' +  device[4][1]
            table.setCellWidget(row, 3, self.get_label(
                table, device_name + ':Pressure-RB-s'))
            table.setCellWidget(row, 4, self.get_label(
                table, device_name + ':Pressure-RB.STAT'))

            device_name = 'ca://' +  device[4][2]
            table.setCellWidget(row, 5, self.get_label(
                table, device_name + ':Pressure-RB-s'))
            table.setCellWidget(row, 6, self.get_label(
                table, device_name + ':Pressure-RB.STAT'))

            device_name = 'ca://' +  device[4][3]
            table.setCellWidget(row, 7, self.get_label(
                table, device_name + ':Pressure-RB-s'))
            table.setCellWidget(row, 4, self.get_label(
                table, device_name + ':Pressure-RB.STAT',))

            device_name = 'ca://' +  device[4][4]
            table.setCellWidget(row, 9, self.get_label(
                table, device_name + ':Pressure-RB-s'))
            table.setCellWidget(row, 10, self.get_label(
                table, device_name + ':Pressure-RB.STAT'))

            device_name = 'ca://' +  device[4][5]
            table.setCellWidget(row, 11, self.get_label(
                table, device_name + ':Pressure-RB-s'))
            table.setCellWidget(row, 12, self.get_label(
                table, device_name + ':Pressure-RB.STAT'))

            device_name = 'ca://' +  device[0]
            table.setCellWidget(row, 13, self.get_label(
                table, device_name + ':Unit', 'Unit'))

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
