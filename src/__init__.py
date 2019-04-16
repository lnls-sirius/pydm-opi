#!/usr/bin/python3
from os import path
from pydm import Display, PyDMApplication
from pydm.utilities import IconFont
from pydm.widgets import PyDMRelatedDisplayButton, PyDMEmbeddedDisplay, PyDMLabel, PyDMByteIndicator


from src.paths import TABLE_ALARMS_QSS, get_abs_path

from PyQt5.QtWidgets import QHeaderView, QLabel, QTableWidgetItem, QWidget, QHBoxLayout, QStyleFactory
from PyQt5.QtCore import pyqtSlot, Qt, QThread, QObject, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5 import QtCore, QtGui, QtWidgets

def get_label(parent, content, tooltip, displayFormat=PyDMLabel.DisplayFormat.Default, precision = None):
    lbl = PyDMLabel(parent=parent, init_channel=content)
    lbl.precisionFromPV = False
    lbl.precision = 2
    lbl.displayFormat = displayFormat
    lbl.showUnits = True
    lbl.alarmSensitiveBorder = True
    lbl.alarmSensitiveContent = True
    lbl.setStyleSheet(TABLE_ALARMS_QSS)
    if precision:
        lbl.precision_changed(precision)
    return lbl

def get_byte_indicator(parent, content, tooltip, **kwargs):
    byte = PyDMByteIndicator(parent, content)
    byte.offColor = QColor(59, 0, 0)
    byte.onColor = QColor(255, 0, 0)
    byte.showLabels = False
    byte.orientation = Qt.Horizontal
    byte.numBits = 12
    return byte


class FlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=-1, hspacing=-1, vspacing=-1):
        super(FlowLayout, self).__init__(parent)
        self._hspacing = hspacing
        self._vspacing = vspacing
        self._items = []
        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self):
        del self._items[:]

    def addItem(self, item):
        self._items.append(item)

    def horizontalSpacing(self):
        if self._hspacing >= 0:
            return self._hspacing
        else:
            return self.smartSpacing(
                QtWidgets.QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self._vspacing >= 0:
            return self._vspacing
        else:
            return self.smartSpacing(
                QtWidgets.QStyle.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)

    def expandingDirections(self):
        return QtCore.Qt.Orientations(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QtCore.QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QtCore.QSize(left + right, top + bottom)
        return size

    def doLayout(self, rect, testonly):
        left, top, right, bottom = self.getContentsMargins()
        effective = rect.adjusted(+left, +top, -right, -bottom)
        x = effective.x()
        y = effective.y()
        lineheight = 0
        for item in self._items:
            widget = item.widget()
            hspace = self.horizontalSpacing()
            if hspace == -1:
                hspace = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton,
                    QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Horizontal)
            vspace = self.verticalSpacing()
            if vspace == -1:
                vspace = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton,
                    QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Vertical)
            nextX = x + item.sizeHint().width() + hspace
            if nextX - hspace > effective.right() and lineheight > 0:
                x = effective.x()
                y = y + lineheight + vspace
                nextX = x + item.sizeHint().width() + hspace
                lineheight = 0
            if not testonly:
                item.setGeometry(
                    QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))
            x = nextX
            lineheight = max(lineheight, item.sizeHint().height())
        return y + lineheight - rect.y() + bottom

    def smartSpacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()

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
