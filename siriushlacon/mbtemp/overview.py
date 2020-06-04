#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from pydm import Display, PyDMApplication
from pydm.utilities import IconFont
from qtpy.QtWidgets import QLabel

from siriushlacon.mbtemp.consts import lazy_devices, OVERVIEW_MAIN_UI
from siriushlacon.utils.widgets import get_label, TableDataController

logger = logging.getLogger()
DEVICES = lazy_devices.get()


class MBTempTableDataController(TableDataController):
    def init_table(self):
        self.table.setRowCount(self.table_batch)
        self.table.setColumnCount(len(self.horizontalHeaderLabels))
        self.table.setHorizontalHeaderLabels(self.horizontalHeaderLabels)
        for actual_row in range(self.table_batch):
            # Channel Name
            self.table.setCellWidget(actual_row, 0, QLabel(""))
            # Device Name
            self.table.setCellWidget(actual_row, 1, QLabel(""))
            # Device Alpha
            self.table.setCellWidget(actual_row, 2, get_label(self.table, "", ""))
            # Temperature
            self.table.setCellWidget(actual_row, 3, get_label(self.table, "", ""))
            # Temperature Raw
            # self.table.setCellWidget(actual_row, 4, get_label(self.table, "", ""))

    def filter(self, pattern):
        if pattern != self.filter_pattern:
            self.filter_pattern = pattern if pattern is not None else ""
            self.batch_offset = 0
            self.filter_pattern = pattern

            for data in self.table_data:
                data[2] = (
                    self.filter_pattern in data[0] or self.filter_pattern in data[1]
                )
            self.update_content.emit()

    def load_table_data(self):
        self.table_data = []
        for device in self.devices:
            if not device.enable:
                continue
            for channel in device.channels:
                if not channel.enable:
                    continue
                self.table_data.append([channel.prefix, device.prefix, True])
        self.update_content.emit()

    def update_table_content(self):
        total_rows = len(self.table_data) * 4

        # Maximum Allowed
        if self.batch_offset >= total_rows:
            return

        # Adding New Content
        actual_row = 0
        dataset_row = 0
        self.table.setVerticalHeaderLabels(
            [
                str(i)
                for i in range(self.batch_offset, self.table_batch + self.batch_offset)
            ]
        )

        for channel, dev, render in self.table_data:
            if channel[-3:-1] == "CH" or actual_row == self.table_batch:
                continue

            # To render or not to render  ...
            if render and dataset_row >= self.batch_offset:
                self.table.setRowHidden(actual_row, False)
                # Channel Access
                device_ca = "ca://" + dev
                channel_ca = "ca://" + channel

                # Channel
                self.table.cellWidget(actual_row, 0).setText(channel)
                # Device
                self.table.cellWidget(actual_row, 1).setText(dev)
                # Alpha
                self.connect_widget(
                    actual_row, 2, device_ca + ":Alpha", connect_color=True
                )
                # Temp
                self.connect_widget(actual_row, 3, channel_ca, connect_color=True)
                # self.connect_widget(actual_row, 4, channel_ca + "-Raw")

                actual_row += 1

            dataset_row += 1

        for row in range(actual_row, self.table_batch):
            self.table.setRowHidden(row, True)

    def update_TempMaxMin(self, Maximum="", Minimum=""):
        if Maximum != "":
            self.MaxValue = Maximum
        if Minimum != "":
            self.MinValue = Minimum


class TableDisplay(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(TableDisplay, self).__init__(parent=parent, args=args, macros=macros)

        table_batch = 0
        for device in DEVICES:
            if not device.enable:
                continue
            for channel in device.channels:
                if not channel.enable:
                    continue
                table_batch += 1

        horizontal_header_labels = [
            "Channel Name",
            "Device Name",
            "Device Alpha",
            "Temperature",
        ]
        # "Temperature Raw",]

        self.tdc = MBTempTableDataController(
            self.table,
            devices=DEVICES,
            table_batch=table_batch,
            horizontal_header_labels=horizontal_header_labels,
        )

        self.tfFilter.editingFinished.connect(lambda: self.filter(self.tfFilter.text()))

        self.TempMax.valueChanged.connect(
            lambda: self.tdc.update_TempMaxMin(Maximum=self.TempMax.value())
        )

        self.TempMin.valueChanged.connect(
            lambda: self.tdc.update_TempMaxMin(Minimum=self.TempMin.value())
        )

        self.btnNavLeft.clicked.connect(lambda: self.update_navbar(False))
        self.btnNavLeft.setIcon(IconFont().icon("arrow-left"))
        self.btnNavRight.clicked.connect(lambda: self.update_navbar(True))
        self.btnNavRight.setIcon(IconFont().icon("arrow-right"))
        PyDMApplication.instance().hide_nav_bar = True

    def update_navbar(self, increase=True):
        self.tdc.changeBatch(increase)

    def filter(self, pattern):
        self.tdc.filter(pattern)

    def ui_filename(self):
        return OVERVIEW_MAIN_UI

    def ui_filepath(self):
        return OVERVIEW_MAIN_UI
