#!/usr/bin/python3
from os import path
from pydm import Display, PyDMApplication
from pydm.utilities import IconFont
from pydm.widgets import PyDMRelatedDisplayButton, PyDMEmbeddedDisplay, PyDMLabel, PyDMByteIndicator

from PyQt5.QtWidgets import QHeaderView, QLabel, QTableWidgetItem, QWidget, QHBoxLayout, QStyleFactory
from PyQt5.QtCore import pyqtSlot, Qt, QThread, QObject, pyqtSignal
from PyQt5.QtGui import QColor

def get_label(parent, content, tooltip, displayFormat=PyDMLabel.DisplayFormat.Default, precision = None):
    lbl = PyDMLabel(parent=parent, init_channel=content)
    lbl.precisionFromPV = False
    lbl.precision = 2
    lbl.displayFormat = displayFormat
    lbl.showUnits = True
    if precision:
        lbl.precision_changed(precision)
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

    table_batch = 24
    filter_pattern = None

    def __init__(self,
            table, devices = [],
            table_batch = 24,
            horizontal_header_labels=[],
            *args, **kwargs):

        super().__init__()
        self.table_data = []
        self.devices = devices
        self.table = table
        self.table_batch = table_batch
        self.horizontalHeaderLabels = horizontal_header_labels

        self.batch_offset = 0

        self.init_table()
        self.update_content.connect(self.update_table_content)
        self.update_content.connect(self.resize)

        self.load_table_data()

    def resize(self):
        if self.table:
            self.table.resizeColumnsToContents()

    def init_table(self):
        self.table.setRowCount(self.table_batch)
        self.table.setColumnCount(len(self.horizontalHeaderLabels))
        self.table.setHorizontalHeaderLabels(self.horizontalHeaderLabels)

        # TODO: Impplement ...
        raise NotImplementedError("Subclass must implement abstract method")

    def filter(self, pattern):
         # TODO: Impplement ...
        raise NotImplementedError("Subclass must implement abstract method")

    def load_table_data(self):
         # TODO: Impplement ...
        raise NotImplementedError("Subclass must implement abstract method")

    def update_table_content(self):
         # TODO: Impplement ...
        raise NotImplementedError("Subclass must implement abstract method")



    def connect_widget(self, row, col, channel_name = None, macros=None):
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
                self.batch_offset += self.table_batch
                self.update_content.emit()
        else:
            if self.batch_offset != 0:
                self.batch_offset -= self.table_batch
                if self.batch_offset < 0:
                    self.batch_offset = 0
                self.update_content.emit()
