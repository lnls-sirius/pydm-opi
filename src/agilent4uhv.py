#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re

from concurrent.futures import ThreadPoolExecutor
from os import path
from pydm import Display, PyDMApplication
from pydm.utilities import IconFont
from pydm.widgets import PyDMRelatedDisplayButton, PyDMEmbeddedDisplay, PyDMLabel, PyDMByteIndicator

from PyQt5.QtWidgets import QComboBox, QLabel, QTableWidgetItem, QWidget, QHBoxLayout, QStyleFactory
from PyQt5.QtCore import pyqtSlot, Qt, QThread, QObject, pyqtSignal
from PyQt5.QtGui import QColor

from src.consts.agilent4uhv import devices
from src.paths import get_abs_path, AGILENT_MAIN_UI, AGILENT_DEVICE_MAIN_UI

ALARM, CURRENT, PRESSURE, VOLTAGE, TEMPERATURE, DEVICE_NAME, CH_CONFIG, AUTOSTART = range(8)
BOOSTER, RING, BTS, LTB = range(4)

EXECUTOR = ThreadPoolExecutor(max_workers=4)

def get_label(parent, content, tooltip, displayFormat=PyDMLabel.DisplayFormat.Default): 
    lbl = PyDMLabel(parent=parent, init_channel=content)
    lbl.precisionFromPV = False
    lbl.precision = 4
    lbl.displayFormat = displayFormat
    lbl.showUnits = True 
    return lbl

def get_byte_indicator(parent, content, tooltip, LSB=True):
    byte = PyDMByteIndicator(parent, content)
    byte.offColor = QColor(59, 0, 0)
    byte.onColor = QColor(255, 0, 0)
    byte.showLabels = False
    byte.orientation = Qt.Horizontal
    if LSB:
        byte.numBits = 8
    else:
        byte.numBits = 4
        byte.shift = 8 
    return byte

class TableDataController(QObject):
    update_content = pyqtSignal()
    TABLE_BATCH = 24
    FILTER_PATTERN = None

    def __init__(self, table, *args, **kwargs):
        super().__init__()
        self.table_data = []
        self.table = table

        self.batch_offset = 0

        if len(devices) * 4 < self.TABLE_BATCH:
            self.TABLE_BATCH = len(devices) * 4
            
        self.init_table()
        self.update_content.connect(self.update_table_content)

        EXECUTOR.submit(lambda: self.load_table_data())

    def init_table(self):
        self.table.setRowCount(self.TABLE_BATCH)
        self.horizontalHeaderLabels = [
                'Channel Name',             # 0
                'Device Name',              # 1
                'Unit',                     # 2
                'Fan Temperature',          # 3
                'Autostart',                # 4

                'Pressure',                 # 5
                'Voltage',                  # 6
                'Current',                  # 7
                'Temperature',              # 8
                'Error Code Mon LSB',       # 9
                'Error Code Mon MSB',       # 10

                'HV State',                 # 11
                'Power Max',                # 12
                'V Target',                 # 13
                'I Protect',                # 14
                'Setpoint',                 # 15
                

                'Details']

        self.table.setColumnCount(len(self.horizontalHeaderLabels))
        self.table.setHorizontalHeaderLabels(self.horizontalHeaderLabels)
                
        for actual_row in range(self.TABLE_BATCH):
                # Channel Name
                self.table.setCellWidget(actual_row, 0, QLabel(''))
                # Device Name
                self.table.setCellWidget(actual_row, 1, QLabel(''))
                # Device Unit
                self.table.setCellWidget(actual_row, 2, get_label(self.table, '', ''))
                # Fan Temperature
                self.table.setCellWidget(actual_row, 3, get_label(self.table, '', ''))
                # Autostart
                self.table.setCellWidget(actual_row, 4, get_label(self.table, '', ''))

                # Pressure
                self.table.setCellWidget(actual_row, 5, get_label(self.table, '', '', PyDMLabel.DisplayFormat.Exponential))
                # Voltage
                self.table.setCellWidget(actual_row, 6, get_label(self.table, '', ''))
                # Current
                self.table.setCellWidget(actual_row, 7, get_label(self.table,'', '', PyDMLabel.DisplayFormat.Exponential))
                # Temperature
                self.table.setCellWidget(actual_row, 8, get_label(self.table, '', '',))
                # LSB
                self.table.setCellWidget(actual_row, 9, get_byte_indicator(self.table, '', ''))
                # MSB
                self.table.setCellWidget(actual_row, 10, get_byte_indicator(self.table, '', '', LSB=False))
                rel = PyDMRelatedDisplayButton(self.table, get_abs_path(AGILENT_DEVICE_MAIN_UI))
                rel.openInNewWindow = True

                # HV State
                self.table.setCellWidget(actual_row, 11, get_label(self.table, '', '',))
                # Power Max
                self.table.setCellWidget(actual_row, 12, get_label(self.table, '', '',))
                # V Target
                self.table.setCellWidget(actual_row, 13, get_label(self.table, '', '',))
                # I Protect
                self.table.setCellWidget(actual_row, 14, get_label(self.table, '', '',))
                # Setpoint
                self.table.setCellWidget(actual_row, 15, get_label(self.table, '', '',))
                
                # Details
                self.table.setCellWidget(actual_row, 16, rel)

    def showHideColumn(self, _type, HIDE):
        if _type == ALARM:
            self.table.setColumnHidden(9, HIDE)
            self.table.setColumnHidden(10, HIDE)
        elif _type == CURRENT:
            self.table.setColumnHidden(7, HIDE)
        elif _type == PRESSURE:
            self.table.setColumnHidden(5, HIDE)
        elif _type == VOLTAGE:
            self.table.setColumnHidden(6, HIDE)
        elif _type == TEMPERATURE:
            self.table.setColumnHidden(8, HIDE)
        elif _type == DEVICE_NAME:
            self.table.setColumnHidden(1, HIDE)
        elif _type == AUTOSTART:
            self.table.setColumnHidden(4, HIDE)
        elif _type == CH_CONFIG:
            for index in range(11,16):
                self.table.setColumnHidden(index, HIDE)

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

    def load_table_data(self):
        for device in devices:
            for ch in range(1, 5):
                aux = [device, ch, True]
                self.table_data.append(aux)
        self.update_content.emit()

    def update_table_content(self):
        total_rows = len(self.table_data) * 4

        # Maximum Allowed
        if self.batch_offset >= total_rows:
            return 

        # Adding New Content
        actual_row = 0
        dataset_row = 0

        self.table.setVerticalHeaderLabels([str(i) for i in range(self.batch_offset, self.TABLE_BATCH + self.batch_offset)])
        for device, devNum, render in self.table_data:

            # To render or not to render  ...
            if render and dataset_row >= self.batch_offset and actual_row != self.TABLE_BATCH:               
                self.table.setRowHidden(actual_row, False)

                # Channel Access
                device_ca = 'ca://' + device[0]
                channel_ca = 'ca://' + device[devNum]
                
                # Datails Button Macro
                macros = '{"DEVICE":"' + device[0] + \
                    '", "PREFIX_C1":"' + device[1] + \
                    '", "PREFIX_C2":"' + device[2] + \
                    '", "PREFIX_C3":"' + device[3] + \
                    '", "PREFIX_C4":"' + device[4] + '"}'
                
                # Channel Name
                self.table.cellWidget(actual_row, 0).setText(device[devNum])
                # Device Name
                self.table.cellWidget(actual_row, 1).setText(device[0])
                # Device Unit
                self.connect_widget(actual_row, 2, device_ca + ':Unit-RB')
                # Fan Temperature
                self.connect_widget(actual_row, 3, device_ca + ':FanTemperature-Mon')
                # Mode-RB
                self.connect_widget(actual_row, 4, device_ca + ':Mode-RB')

                # Pressure
                self.connect_widget(actual_row, 5,  channel_ca + ':Pressure-Mon')
                # Voltage
                self.connect_widget(actual_row, 6, channel_ca + ':Voltage-Mon')
                # Current
                self.connect_widget(actual_row, 7, channel_ca + ':Current-Mon')
                # Temperature
                self.connect_widget(actual_row, 8, channel_ca + ':HVTemperature-Mon')
                # LSB
                self.connect_widget(actual_row, 9, channel_ca + ':ErrorCode-Mon')
                # MSB
                self.connect_widget(actual_row, 10, channel_ca + ':ErrorCode-Mon')
                
                # HVState-RB
                self.connect_widget(actual_row, 11, channel_ca + ':HVState-RB')
                # PowerMax-RB
                self.connect_widget(actual_row, 12, channel_ca + ':PowerMax-RB')
                # VoltageTarget-RB
                self.connect_widget(actual_row, 13, channel_ca + ':VoltageTarget-RB')
                # CurrentProtect-RB
                self.connect_widget(actual_row, 14, channel_ca + ':CurrentProtect-RB')
                # Setpoint-RB
                self.connect_widget(actual_row, 15, channel_ca + ':Setpoint-RB')


                # Details
                self.connect_widget(actual_row, 16, None, macros)

                actual_row += 1
            dataset_row += 1

            if actual_row != self.TABLE_BATCH:
                for row in range(actual_row, self.TABLE_BATCH):
                    self.table.setRowHidden(row, True)

    def connect_row(self, row, dev_name, ch_name, dev_ca, ch_ca, macro):
        # Channel Name
        self.table.cellWidget(row, 0).setText(ch_name)
        # Device Name
        self.table.cellWidget(row, 1).setText(dev_name)
        # Device Unit
        self.connect_widget(row, 2, dev_ca + ':Unit-RB')
        # Pressure
        self.connect_widget(row, 3,  ch_ca + ':Pressure-Mon')
        # Voltage
        self.connect_widget(row, 4, ch_ca + ':Voltage-Mon')
        # Current
        self.connect_widget(row, 5, ch_ca + ':Current-Mon')
        # Temperature
        self.connect_widget(row, 6, ch_ca + ':HVTemperature-Mon')
        # LSB
        self.connect_widget(row, 7, ch_ca + ':ErrorCode-Mon')
        # MSB
        self.connect_widget(row, 8, ch_ca + ':ErrorCode-Mon')
        # Details
        self.connect_widget(row, 9, None, macro)
        
    def connect_widget(self, row, col, channel_name, macros=None):
        widget = self.table.cellWidget(row, col)
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
        
        self.tdc = TableDataController(self.table)

        self.chAlarms.stateChanged.connect(lambda: self.showHideColumn(ALARM, self.chAlarms))
        self.chCurrent.stateChanged.connect(lambda: self.showHideColumn(CURRENT, self.chCurrent))
        self.chPressure.stateChanged.connect(lambda: self.showHideColumn(PRESSURE, self.chPressure))
        self.chVoltage.stateChanged.connect(lambda: self.showHideColumn(VOLTAGE, self.chVoltage))
        self.chTemperature.stateChanged.connect(lambda: self.showHideColumn(TEMPERATURE, self.chTemperature))
        self.chDeviceName.stateChanged.connect(lambda: self.showHideColumn(DEVICE_NAME, self.chDeviceName))
        self.chChConfig.stateChanged.connect(lambda: self.showHideColumn(CH_CONFIG, self.chChConfig))
        self.chAutostart.stateChanged.connect(lambda: self.showHideColumn(AUTOSTART, self.chAutostart))

        self.tfFilter.editingFinished.connect(
            lambda: self.filter(self.tfFilter.text()))

        self.btnNavLeft.clicked.connect(lambda: self.update_navbar(False))
        self.btnNavLeft.setIcon(IconFont().icon('arrow-left'))
        self.btnNavRight.clicked.connect(lambda: self.update_navbar(True))
        self.btnNavRight.setIcon(IconFont().icon('arrow-right'))
    
    def update_navbar(self, increase = True):
        self.tdc.changeBatch(increase)

    def filter(self, pattern):
        self.tdc.filter(pattern)

    def showHideColumn(self, _type, chk):
        HIDE = not chk.isChecked()
        self.tdc.showHideColumn(_type, HIDE)

    def ui_filename(self):
        return AGILENT_MAIN_UI

    def ui_filepath(self):
        return get_abs_path(AGILENT_MAIN_UI)
