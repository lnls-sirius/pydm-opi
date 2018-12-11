#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from os import path

from pydm import Display
from pydm.widgets import PyDMRelatedDisplayButton, PyDMEmbeddedDisplay, PyDMLabel

from PyQt5.QtWidgets import QComboBox, QLabel, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal

from src.consts.mks937b import devices, COLD_CATHODE, PIRANI

from src.paths import get_abs_path, TABLE_UI, DEVICE_MENU


class StorageRing(Display):
    update_content = pyqtSignal()

    def __init__(self, parent=None, args=[], macros=None):
        super(StorageRing, self).__init__(
            parent=parent, args=args, macros=macros)
        self.config_table(self.boosterTableWidget, devices)
        self.update_content.connect(self.update_table_content)

        #self.tfFilter.editingFinished.connect(
        #            lambda: self.filter(self.tfFilter.text()))

        def filter(self, pattern):
                if not pattern:
                    pattern = ""
                if pattern != self.FILTER_PATTERN:
                    self.batch_offset = 0
                    self.FILTER_PATTERN = pattern
                    try:
                        for data in self.table_data:
                            RENDER = self.FILTER_PATTERN in data[0][0] or self.FILTER_PATTERN in data[0][data[1]]
                            data[2] = RENDER
                        self.update_content.emit()
                    except:
                        pass

    def update_table_content(self):
        # Todo!
        pass

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
            'Gauge',
            'Device',
            'Pressure',
            'Alarm',
            'Unit',
            'Details']

        table.setRowCount(len(devices)*6)
        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

        row = 0
        for data in devices:
            device_name = data[0]
            for gauge in data[4]:
                gauge_ca = 'ca://' +  gauge

                table.setCellWidget(row, 0, QLabel(gauge))
                table.setCellWidget(row, 1, QLabel(device_name))

                self.add_label(table, row, 2, gauge_ca + ':Pressure-Mon-s')
                self.add_label(table, row, 3, gauge_ca + ':Pressure-Mon.STAT')

                self.add_label(table, row, 4, device_name + ':Unit', 'Unit')


                rel = PyDMRelatedDisplayButton(table, get_abs_path(DEVICE_MENU))
                rel.openInNewWindow = True
                rel.macros = \
                '{"DEVICE" :"' +  device_name + '",\
                "G1":"' + data[4][0] + '",\
                "G2":"' + data[4][1] + '",\
                "G3":"' + data[4][2] + '",\
                "G4":"' + data[4][3] + '",\
                "G5":"' + data[4][4] + '",\
                "G6":"' + data[4][5] + '",\
                "A":"' + data[1] + '",\
                "B":"' + data[2] + '", \
                "C":"' + data[3] + '"}'
                table.setCellWidget(row, 5, rel)

                row += 1

    def ui_filename(self):
        return TABLE_UI

    def ui_filepath(self):
        return get_abs_path(TABLE_UI)
