#!/usr/bin/env python3
import sys
from typing import List

from qtpy import QtGui, QtWidgets

from conscommon.data import getAgilent
from conscommon.data_model import (
    getDevicesFromList,
    getBeaglesFromList,
    getDevicesFromBeagles,
    Device,
)

class DeviceTreeSelection(object):
    def __init__(self, device: Device, channels_selected: List[bool]):
        self.device = device
        self.channels_selected = channels_selected

class DeviceTreeView(QtWidgets.QWidget):
    def __init__(self):
        super(DeviceTreeView, self).__init__()

        self.tree = QtWidgets.QTreeView(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tree)

        self.model = QtGui.QStandardItemModel()
        self.model.dataChanged.connect(self.itemChanged)

        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        self.model.itemChanged.connect(self.itemChanged)

        self.button = QtWidgets.QPushButton("Get")
        self.button.clicked.connect(self.getData)
        layout.addWidget(self.button)

        self.cont = True

    def importData(self, data: List[Device], root=None):

        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Device", "Channel"])
        self.model.setRowCount(0)

        count = 0
        if root is None:
            root = self.model.invisibleRootItem()

        for d in data:
            item_dev = QtGui.QStandardItem(d.prefix)
            item_dev.setAutoTristate(False)
            item_dev.setCheckable(True)
            item_dev.setEditable(False)
            item_dev.setUserTristate(False)

            for ch in d.channels:
                i_ = QtGui.QStandardItem(ch.name)
                i_.setAutoTristate(False)
                i_.setCheckable(True)
                i_.setEditable(False)
                i_.setUserTristate(False)

                i_p = QtGui.QStandardItem(ch.prefix)
                i_p.setEditable(False)

                item_dev.appendRow([i_, i_p])

            root.appendRow(item_dev)
            count += 1
        self.model.setRowCount(count)

    def checkParentState(self, item) -> int:
        checked = 0
        for row in range(item.rowCount()):
            if item.child(row, 0).checkState() != 0:
                checked += 1

        if checked == item.rowCount():
            return 2
        elif checked == 0:
            return 0
        else:
            return 1

    def getData(self) -> List[DeviceTreeSelection]:
        root = self.model.invisibleRootItem()
        selected: List[DeviceTreeSelection] = []

        # Loop through devices
        for i in range(root.rowCount()):
            row = root.child(i, 0)

            if row.isCheckable() and row.checkState() != 0:
                channels = {}
                channels_selected = []
                for j in range(row.rowCount()):
                    channels_selected.append(row.child(j, 0).checkState() != 0)
                    channels[row.child(j, 0).text()] = {
                        "prefix": row.child(j, 1).text()
                    }

                selected.append(
                    DeviceTreeSelection(
                        Device(prefix=row.text(), channels=channels),
                        channels_selected
                    )
                )
        return selected

    def paintItem(self, item, state):
        if state == 0:
            item.setBackground(QtGui.QColor("#fffff2"))
        elif state == 1:
            item.setBackground(QtGui.QColor("#ffffb2"))
        elif state == 2:
            item.setBackground(QtGui.QColor("#c0ffb2"))

    def iterChild(self, item):
        for row in range(item.rowCount()):
            yield item.child(row, 0), item.child(row, 1)

    def itemChanged(self, item):

        if not self.cont:
            return

        if type(item) == QtGui.QStandardItem:
            self.cont = False
            parent = item.parent()

            if item.rowCount() > 0 and parent is None:
                if item.checkState() == 0 or item.checkState() == 2:
                    for row in range(item.rowCount()):
                        if item.child(row, 0).checkState() != item.checkState():
                            item.child(row, 0).setCheckState(item.checkState())
            else:
                if parent and parent.isCheckable():
                    state = self.checkParentState(parent)
                    parent.setCheckState(state)

            _p = item if (parent is None and item.rowCount() > 0) else parent
            self.paintItem(_p, _p.checkState())
            for i1, i2 in self.iterChild(
                item if (parent is None and item.rowCount() > 0) else parent
            ):
                self.paintItem(i1, i1.checkState())
                self.paintItem(i2, i1.checkState())
            self.cont = True


if __name__ == "__main__":

    data = getDevicesFromBeagles(getBeaglesFromList(getAgilent()))

    app = QtWidgets.QApplication(sys.argv)
    window = DeviceTreeView(data)
    window.setGeometry(600, 50, 400, 250)
    window.show()
    sys.exit(app.exec_())
