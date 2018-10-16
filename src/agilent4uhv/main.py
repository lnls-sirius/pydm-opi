#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re

from concurrent.futures import ThreadPoolExecutor

from os import path
from pydm import Display, PyDMApplication
from pydm.utilities import IconFont
from pydm.widgets import PyDMRelatedDisplayButton, PyDMEmbeddedDisplay, PyDMLabel, PyDMByteIndicator
from PyQt5.QtWidgets import QComboBox, QLabel, QTableWidgetItem, QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSlot, Qt, QThread, QObject, pyqtSignal

from src.agilent4uhv.consts import ring_sector_devices, booster_sector_devices, bts_sector_devices, ltb_sector_devices
from src.paths import get_abs_path, AGILENT_MAIN_UI, AGILENT_DEVICE_MAIN_UI

ALARM, CURRENT, PRESSURE, VOLTAGE, TEMPERATURE, DEVICE_NAME = range(6)
BOOSTER, RING, BTS, LTB = range(4)

EXECUTOR = ThreadPoolExecutor(max_workers=4)

 
def get_label(parent, content, tooltip, displayFormat=PyDMLabel.DisplayFormat.Default):
    lbl = PyDMLabel(parent=parent, init_channel=content)
    lbl.precisionFromPV = False
    lbl.precision = 4
    lbl.displayFormat = displayFormat
    lbl.showUnits = True
    # PyDMApplication.instance().establish_widget_connections(lbl)
    return lbl

def get_byte_indicator(parent, content, tooltip, LSB=True):
    byte = PyDMByteIndicator(parent, content)
    byte.showLabels = False
    byte.orientation = Qt.Horizontal
    if LSB:
        byte.numBits = 8
    else:
        byte.numBits = 4
        byte.shift = 8
    # PyDMApplication.instance().establish_widget_connections(byte)
    return byte

class TableDataController(QObject):

    update_content = pyqtSignal()

    TABLE_BATCH = 20
    FILTER_PATTERN = None

    def __init__(self, table, table_type):
        super().__init__()
        self.table_data = []
        self.devices = []
        self.table = table

        self.batch_offset = 0

        if table_type == BOOSTER:
            self.devices = booster_sector_devices
        elif table_type == RING:
            self.devices = ring_sector_devices
        elif table_type == BTS:
            self.devices = bts_sector_devices
        elif table_type == LTB:
            self.devices = ltb_sector_devices

        if len(self.devices) < self.TABLE_BATCH:
            self.TABLE_BATCH = len(self.devices)
            
        self.init_table()
        self.update_content.connect(self.update_table_content)

        EXECUTOR.submit(lambda: self.load_table_data())

    def init_table(self):
        self.table.setRowCount(self.TABLE_BATCH)
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(
            [
                'Channel Name',             # 0
                'Device Name',              # 1
                'Unit',                     # 2

                'Pressure',                 # 3
                'Voltage',                  # 4
                'Current',                  # 5
                'Temperature',              # 6
                'Error Code Mon LSB',       # 7
                'Error Code Mon MSB',       # 8

                'Details'])                 # 9
                
        for actual_row in range(self.TABLE_BATCH):
                # Channel Name
                self.table.setCellWidget(actual_row, 0, QLabel(''))
                # Device Name
                self.table.setCellWidget(actual_row, 1, QLabel(''))
                # Device Unit
                self.table.setCellWidget(actual_row, 2, get_label(self.table, '', ''))
                # Pressure
                self.table.setCellWidget(actual_row, 3, get_label(self.table, '', '', PyDMLabel.DisplayFormat.Exponential))
                # Voltage
                self.table.setCellWidget(actual_row, 4, get_label(self.table, '', ''))
                # Current
                self.table.setCellWidget(actual_row, 5, get_label(self.table,'', '', PyDMLabel.DisplayFormat.Exponential))
                # Temperature
                self.table.setCellWidget(actual_row, 6, get_label(self.table, '', '',))
                # LSB
                self.table.setCellWidget(actual_row, 7, get_byte_indicator(self.table, '', ''))
                # MSB
                self.table.setCellWidget(actual_row, 8, get_byte_indicator(self.table, '', '', LSB=False))
                rel = PyDMRelatedDisplayButton(self.table, get_abs_path(AGILENT_DEVICE_MAIN_UI))
                rel.openInNewWindow = True
                # Details
                self.table.setCellWidget(actual_row, 9, rel)

    def showHideColumn(self, _type, HIDE):
        if _type == ALARM:
            self.table.setColumnHidden(7, HIDE)
            self.table.setColumnHidden(8, HIDE)
        elif _type == CURRENT:
            self.table.setColumnHidden(5, HIDE)
        elif _type == PRESSURE:
            self.table.setColumnHidden(3, HIDE)
        elif _type == VOLTAGE:
            self.table.setColumnHidden(4, HIDE)
        elif _type == TEMPERATURE:
            self.table.setColumnHidden(6, HIDE)
        elif _type == DEVICE_NAME:
            self.table.setColumnHidden(1, HIDE)

    def filter(self, pattern):
        if not pattern:
            pattern = ""
        if pattern != self.FILTER_PATTERN:
            self.batch_offset = 0
            self.FILTER_PATTERN = pattern
            try:
                regex = re.compile(self.FILTER_PATTERN, re.I | re.U)
                # data[0] -> Devices
                # data[1] -> Channel Num
                # data[2] -> To render or not
                for data in self.table_data:
                    RENDER = not \
                        (
                            regex.match(data[0][0]) == None
                            and
                            regex.match(data[0][data[1]]) == None
                        )
                    data[2] = RENDER
                self.update_content.emit()
            except:
                pass

    def load_table_data(self):
        for device in self.devices:
            for ch in range(1, 5):
                aux = [device, ch, True]
                self.table_data.append(aux)
        self.update_content.emit()

    def update_table_content(self):
        total_rows = len(self.table_data) * 4

        # Maximum Allowed
        if self.batch_offset >= total_rows:
            return

        # Clear table
        # self.app.close_widget_connections(self.table)
        # self.table.clearContents()

        # Adding New Content
        actual_row = 0
        dataset_row = 0

        self.table.setVerticalHeaderLabels([str(i) for i in range(self.batch_offset, self.TABLE_BATCH + self.batch_offset)])
        for device, devNum, render in self.table_data:

            # To render or not to render  ...
            if render and dataset_row >= self.batch_offset and actual_row != self.TABLE_BATCH:               
                self.table.setRowHidden(actual_row, False)

                # Channel Name
                self.table.cellWidget(actual_row, 0).setText(device[devNum])
                # Device Name
                self.table.cellWidget(actual_row, 1).setText(device[0])
                # Device Unit
                device_name = 'ca://' + device[0]
                self.connect_widget(actual_row, 2, device_name + ':Unit-RB')
                device_name = 'ca://' + device[1]
                # Pressure
                self.connect_widget(actual_row, 3, device_name + ':Pressure-Mon')
                # Voltage
                self.connect_widget(actual_row, 4, device_name + ':Voltage-Mon')
                # Current
                self.connect_widget(actual_row, 5, device_name + ':Current-Mon')
                # Temperature
                self.connect_widget(actual_row, 6, device_name + ':HVTemperature-Mon')
                # LSB
                self.connect_widget(actual_row, 7, device_name + ':ErrorCode-Mon')
                # MSB
                self.connect_widget(actual_row, 8, device_name + ':ErrorCode-Mon')
                # Details
                macros = '{"DEVICE":"' + device[0] + \
                    '", "PREFIX_C1":"' + device[1] + \
                    '", "PREFIX_C2":"' + device[2] + \
                    '", "PREFIX_C3":"' + device[3] + \
                    '", "PREFIX_C4":"' + device[4] + '"}'
                self.connect_widget(actual_row, 9, None, macros)

                actual_row += 1
            dataset_row += 1

            if actual_row != self.TABLE_BATCH:
                for row in range(actual_row, self.TABLE_BATCH):
                    self.table.setRowHidden(row, True)
                
            # New connections ...
            # self.app.establish_widget_connections(self.table)

    def connect_widget(self, row, col, channel_name, macros=None):
        widget = self.table.cellWidget(row, col)
        if widget:
            PyDMApplication.instance().close_widget_connections(widget)
            if channel_name:
                widget.channel = channel_name
            if macros:
                widget.macros = macros
            PyDMApplication.instance().establish_widget_connections(widget)

    def changeBatch(self, increase):
        if increase:
            if self.batch_offset < len(self.table_data):
                self.batch_offset += self.TABLE_BATCH
                self.update_content.emit()
        else:
            if self.batch_offset != 0:
                self.batch_offset -= self.TABLE_BATCH
                if self.batch_offset < 0:
                    self.batch_offset = 0
                self.update_content.emit()

class StorageRing(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(StorageRing, self).__init__(
            parent=parent, args=args, macros=macros)

        self.TABLES = [self.boosterTableWidget, self.ringTableWidget,
                       self.ltbTableWidget, self.btsTableWidget]

        self.boosterTableDataController = TableDataController(self.TABLES[0], BOOSTER)
        self.ringTableDataController = TableDataController(self.TABLES[1], RING)
        self.ltbTableDataController = TableDataController(self.TABLES[2], LTB)
        self.btsTableDataController = TableDataController(self.TABLES[3], BTS)

        self.chAlarms.stateChanged.connect(lambda: self.showHideColumn(ALARM, self.chAlarms))
        self.chCurrent.stateChanged.connect(lambda: self.showHideColumn(CURRENT, self.chCurrent))
        self.chPressure.stateChanged.connect(lambda: self.showHideColumn(PRESSURE, self.chPressure))
        self.chVoltage.stateChanged.connect(lambda: self.showHideColumn(VOLTAGE, self.chVoltage))
        self.chTemperature.stateChanged.connect(lambda: self.showHideColumn(TEMPERATURE, self.chTemperature))
        self.chDeviceName.stateChanged.connect(lambda: self.showHideColumn(DEVICE_NAME, self.chDeviceName))

        self.tfFilter.editingFinished.connect(
            lambda: self.filter(self.tfFilter.text()))

        self.btnNavLeft.clicked.connect(lambda: self.update_navbar(False))
        self.btnNavLeft.setIcon(IconFont().icon('arrow-left'))
        self.btnNavRight.clicked.connect(lambda: self.update_navbar(True))
        self.btnNavRight.setIcon(IconFont().icon('arrow-right'))
    
    def update_navbar(self, increase = True):
        current_nav = self.tabWidget.currentIndex()
        if current_nav == BOOSTER:
            self.boosterTableDataController.changeBatch(increase)
        elif current_nav == RING:
            self.ringTableDataController.changeBatch(increase)
        elif current_nav == LTB:
            self.ltbTableDataController.changeBatch(increase)
        elif current_nav == BTS:
            self.btsTableDataController.changeBatch(increase)

    def update_table_widgets(self, table, offset=0):
        pass

    def filter(self, pattern):
        self.boosterTableDataController.filter(pattern)
        self.ringTableDataController.filter(pattern)
        self.ltbTableDataController.filter(pattern)
        self.btsTableDataController.filter(pattern)

    def showHideColumn(self, _type, chk):
        HIDE = not chk.isChecked()

        self.boosterTableDataController.showHideColumn(_type, HIDE)
        self.ringTableDataController.showHideColumn(_type, HIDE)
        self.ltbTableDataController.showHideColumn(_type, HIDE)
        self.btsTableDataController.showHideColumn(_type, HIDE)

    def ui_filename(self):
        return AGILENT_MAIN_UI

    def ui_filepath(self):
        return get_abs_path(AGILENT_MAIN_UI)
