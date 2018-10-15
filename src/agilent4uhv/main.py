#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re

from os import path
from pydm import Display
from pydm.widgets import PyDMRelatedDisplayButton, PyDMEmbeddedDisplay, PyDMLabel, PyDMByteIndicator

from PyQt5.QtWidgets import QComboBox, QLabel, QTableWidgetItem, QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSlot, Qt 
# from macros import get_device_macro

from src.agilent4uhv.consts import ring_sector_devices, booster_sector_devices, bts_sector_devices, ltb_sector_devices
from src.paths import get_abs_path, AGILENT_MAIN_UI, AGILENT_DEVICE_MAIN_UI

ALARM, CURRENT, PRESSURE, VOLTAGE, TEMPERATURE = range(5)

class StorageRing(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(StorageRing, self).__init__(
            parent=parent, args=args, macros=macros)
       
        self.TABLES = [self.boosterTableWidget, self.ringTableWidget, self.ltbTableWidget, self.btsTableWidget]

        self.config_table(self.boosterTableWidget, booster_sector_devices) 
        self.config_table(self.ringTableWidget, ring_sector_devices) 
        self.config_table(self.ltbTableWidget, ltb_sector_devices) 
        self.config_table(self.btsTableWidget, bts_sector_devices) 
        
        self.chAlarms.stateChanged.connect(lambda:self.showHideColumn(ALARM, self.chAlarms))
        self.chCurrent.stateChanged.connect(lambda:self.showHideColumn(CURRENT, self.chCurrent))
        self.chPressure.stateChanged.connect(lambda:self.showHideColumn(PRESSURE, self.chPressure))
        self.chVoltage.stateChanged.connect(lambda:self.showHideColumn(VOLTAGE, self.chVoltage))
        self.chTemperature.stateChanged.connect(lambda:self.showHideColumn(TEMPERATURE, self.chTemperature))

        self.tfFilter.textChanged.connect(self.filter)

    def filter(self, pattern):
        try:
            if not pattern:
                pattern = ""
            regex = re.compile(pattern, re.I | re.U)

            for table in self.TABLES: 
                for row in range(table.rowCount()):
                    HIDE = not regex.match(table.cellWidget(row, 0).text())
                    table.setRowHidden(row,  HIDE)
        except:
            pass
    
    def showHideColumn(self, _type, chk):
        HIDE = not chk.isChecked()
        for table in self.TABLES:
            if _type == ALARM:
                table.setColumnHidden(6,  HIDE)
                table.setColumnHidden(7, HIDE)
                table.setColumnHidden(12, HIDE)
                table.setColumnHidden(13, HIDE) 
                table.setColumnHidden(18,  HIDE)
                table.setColumnHidden(19, HIDE)
                table.setColumnHidden(24, HIDE)
                table.setColumnHidden(25, HIDE) 
            elif _type == CURRENT:
                table.setColumnHidden(4,  HIDE)
                table.setColumnHidden(10,  HIDE)
                table.setColumnHidden(16, HIDE)
                table.setColumnHidden(22, HIDE)
            elif _type == PRESSURE:
                table.setColumnHidden(2,  HIDE)
                table.setColumnHidden(8,  HIDE)
                table.setColumnHidden(14, HIDE)
                table.setColumnHidden(20, HIDE)
            elif _type == VOLTAGE:
                table.setColumnHidden(3,  HIDE)
                table.setColumnHidden(9,  HIDE)
                table.setColumnHidden(15, HIDE)
                table.setColumnHidden(21, HIDE)
            elif _type == TEMPERATURE:
                table.setColumnHidden(5,  HIDE)
                table.setColumnHidden(11,  HIDE)
                table.setColumnHidden(17, HIDE)
                table.setColumnHidden(23, HIDE)

    def get_label(self, parent, content, tooltip):
        lbl = PyDMLabel(parent, content)
        lbl.setToolTip(tooltip)
        return lbl
    
    def get_byte_indicator(self, parent, content, tooltip, LSB = True): 
        
        byte = PyDMByteIndicator(parent, content)
        byte.showLabels = False
        byte.orientation = Qt.Horizontal
        if LSB:
            byte.numBits = 8
        else:
            byte.numBits = 4
            byte.shift = 8
        return byte
        # @todo: For some reason this approach isn't working ...
        # box = QWidget(parent)
        # box.setLayout(QHBoxLayout())

        # byteA = PyDMByteIndicator(box, content)
        # byteA.numBits = 8
        # byteA.orientation = Qt.Horizontal
        # byteA.showLabels = False
        
        # byteB = PyDMByteIndicator(box, content)
        # byteB.numBits = 4
        # byteB.shift = 8
        # byteB.orientation = Qt.Horizontal
        # byteB.showLabels = False

        # box.layout().addWidget(byteA)
        # box.layout().addWidget(byteB)
        
        # #byteA.resize(byteA.sizeHint());
        # #byteB.resize(byteB.sizeHint());
 
        # byteA.rebuild_layout()
        # byteB.rebuild_layout()

        # box.show()

        # return box
  
    def config_table(self, table, devices):
        num_devices = len(devices)
        
        table.setRowCount(num_devices)
        table.setColumnCount(27)
        table.setHorizontalHeaderLabels(
            ['Device Name',             # 0
            'Unit',                     # 1

            'CH1 - Pressure',           # 2
            'CH1 - Voltage',            # 3
            'CH1 - Current',            # 4
            'CH1 - Temperature',        # 5
            'CH1 - Error Code Mon LSB', # 6
            'CH1 - Error Code Mon MSB', # 7

            'CH2 - Pressure',           # 8
            'CH2 - Voltage',            # 9
            'CH2 - Current',            # 10
            'CH2 - Temperature',        # 11
            'CH2 - Error Code Mon LSB', # 12
            'CH2 - Error Code Mon MSB', # 13

            'CH3 - Pressure',           # 14
            'CH3 - Voltage',            # 15
            'CH3 - Current',            # 16
            'CH3 - Temperature',        # 17
            'CH3 - Error Code Mon LSB', # 18
            'CH3 - Error Code Mon MSB', # 19

            'CH4 - Pressure',           # 20
            'CH4 - Voltage',            # 21
            'CH4 - Current',            # 22
            'CH4 - Temperature',        # 23
            'CH4 - Error Code Mon LSB', # 24
            'CH4 - Error Code Mon MSB', # 25

            'Details'])                 # 26

        for row in range(0, num_devices):
            # PyDMLabel
            device = devices[row]
            
            table.setCellWidget(row, 0, QLabel( device[0]))

            device_name = 'ca://' +  device[0]            
            table.setCellWidget(row, 1, self.get_label(table, device_name + ':Unit-RB', device[0]))

            device_name = 'ca://' +  device[1]
            table.setCellWidget(row, 2, self.get_label(table, device_name + ':Pressure-Mon'     , device[1]))
            table.setCellWidget(row, 3, self.get_label(table, device_name + ':Voltage-Mon'      , device[1]))
            table.setCellWidget(row, 4, self.get_label(table, device_name + ':Current-Mon'      , device[1]))
            table.setCellWidget(row, 5, self.get_label(table, device_name + ':HVTemperature-Mon', device[1]))
            table.setCellWidget(row, 6, self.get_byte_indicator(table, device_name + ':ErrorCode-Mon'    , device[1]))
            table.setCellWidget(row, 7, self.get_byte_indicator(table, device_name + ':ErrorCode-Mon'    , device[1], LSB=False))

            device_name = 'ca://' +  device[2]
            table.setCellWidget(row, 8, self.get_label(table, device_name + ':Pressure-Mon'     , device[2]))
            table.setCellWidget(row, 9, self.get_label(table, device_name + ':Voltage-Mon'      , device[2]))
            table.setCellWidget(row, 10, self.get_label(table, device_name + ':Current-Mon'      , device[2]))
            table.setCellWidget(row, 11, self.get_label(table, device_name + ':HVTemperature-Mon', device[2]))
            table.setCellWidget(row, 12, self.get_byte_indicator(table, device_name + ':ErrorCode-Mon'    , device[2]))
            table.setCellWidget(row, 13, self.get_byte_indicator(table, device_name + ':ErrorCode-Mon'    , device[2], LSB=False))

            device_name = 'ca://' +  device[3]
            table.setCellWidget(row, 14, self.get_label(table, device_name + ':Pressure-Mon'     , device[3]))
            table.setCellWidget(row, 15, self.get_label(table, device_name + ':Voltage-Mon'      , device[3]))
            table.setCellWidget(row, 16, self.get_label(table, device_name + ':Current-Mon'      , device[3]))
            table.setCellWidget(row, 17, self.get_label(table, device_name + ':HVTemperature-Mon', device[3]))
            table.setCellWidget(row, 18, self.get_byte_indicator(table, device_name + ':ErrorCode-Mon'    , device[3]))
            table.setCellWidget(row, 19, self.get_byte_indicator(table, device_name + ':ErrorCode-Mon'    , device[3], LSB=False))
            
            device_name = 'ca://' +  device[4]
            table.setCellWidget(row, 20, self.get_label(table, device_name + ':Pressure-Mon'     , device[4]))
            table.setCellWidget(row, 21, self.get_label(table, device_name + ':Voltage-Mon'      , device[4]))
            table.setCellWidget(row, 22, self.get_label(table, device_name + ':Current-Mon'      , device[4]))
            table.setCellWidget(row, 23, self.get_label(table, device_name + ':HVTemperature-Mon', device[4]))
            table.setCellWidget(row, 24, self.get_byte_indicator(table, device_name + ':ErrorCode-Mon'    , device[4]))
            table.setCellWidget(row, 25, self.get_byte_indicator(table, device_name + ':ErrorCode-Mon'    , device[4], LSB=False))
            
            
            rel = PyDMRelatedDisplayButton(table, get_abs_path(AGILENT_DEVICE_MAIN_UI))
            rel.openInNewWindow = True
            rel.macros = '{"DEVICE":"' + device[0] + '", "PREFIX_C1":"' + device[1] + '", "PREFIX_C2":"' + device[2] + '", "PREFIX_C3":"' + device[3] + '", "PREFIX_C4":"' + device[4] + '"}'
            table.setCellWidget(row, 26, rel)

    def ui_filename(self):
        return AGILENT_MAIN_UI

    def ui_filepath(self):
        return get_abs_path(AGILENT_MAIN_UI)
 