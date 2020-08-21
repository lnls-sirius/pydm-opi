#!/usr/bin/env python3
import logging
from typing import List
from qtpy.QtWidgets import (
    QFrame,
    QGridLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
)
from qtpy.QtGui import QColor
from qtpy.QtCore import Qt

from conscommon.data import getAgilent
from conscommon.data_model import getDevicesFromBeagles, getBeaglesFromList, Device
from siriushlacon.agilent4uhv.tree import DeviceTreeView, DeviceTreeSelection

logger = logging.getLogger()


class DevicesFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super(DevicesFrame, self).__init__(*args, **kwargs)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.contentLayout = QGridLayout()

        self.data: List[Device] = []

        # Current Action Status
        self.status = {}

        self.devicePrefixFilterLabel = QLabel(
            "Device filter (Ion Pump not the channel!)"
        )
        self.devicePrefixFilterInp = QLineEdit()
        self.devicePrefixFilterInp.setMaximumWidth(100)

        self.updateDeviceListButton = QPushButton("Apply Filter")
        self.updateDeviceListButton.clicked.connect(self.updateDeviceList)
        self.updateDeviceListButton.setToolTip("Filter the device prefix list.")

        self.contentLayout.addWidget(self.devicePrefixFilterLabel, 0, 0, 1, 2)
        self.contentLayout.addWidget(self.devicePrefixFilterInp, 1, 0, 1, 1)
        self.contentLayout.addWidget(self.updateDeviceListButton, 1, 1, 1, 1)

        self.deviceList = DeviceTreeView()
        self.contentLayout.addWidget(self.deviceList, 2, 0, 2, 2)

        self.deviceStatus = QTableWidget()
        self.deviceStatus.setColumnCount(2)
        #self.deviceStatus.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.deviceStatus.setHorizontalHeaderLabels(["Device", "Status"])
        self.deviceStatusLabel = QLabel("Status")

        self.contentLayout.addWidget(self.deviceStatusLabel, 0, 2, 1, 2)
        self.contentLayout.addWidget(self.deviceStatus, 1, 2, 4, 2)

        self.contentLayout.setRowStretch(2, 2)

        self.setLayout(self.contentLayout)
        self.reloadData()

    def clearStatus(self):
        self.status = {}
        self.deviceStatus.setRowCount(0)

    def updateStatus(self, param):
        self.status[param["device"]] = "{}".format(param["status"])
        idx = 0
        self.deviceStatus.setRowCount(len(self.status))
        for k, v in self.status.items():
            self.deviceStatus.setItem(idx, 0, QTableWidgetItem(k))
            self.deviceStatus.setItem(idx, 1, QTableWidgetItem(v))
            idx += 1

    def getSelectedDevices(self) -> List[DeviceTreeSelection]:
        return self.deviceList.getData()

    def highlightChecked(self, item):
        if item.checkState() == Qt.Checked:
            item.setBackground(QColor("#ffffb2"))
        else:
            item.setBackground(QColor("#ffffff"))

    def updateDeviceList(self):
        devs = []
        _filter = self.devicePrefixFilterInp.text()
        for d in self.data:
            if _filter == "" or _filter in d.prefix:
                devs.append(d)
        self.deviceList.importData(devs)

    def reloadData(self):
        self.data = getDevicesFromBeagles(getBeaglesFromList(getAgilent()))
        self.deviceList.importData(self.data)
