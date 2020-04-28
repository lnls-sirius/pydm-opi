#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import threading
import json

from typing import List

import epics
from pydm import Display
from pydm.utilities import IconFont
from pydm.widgets import PyDMRelatedDisplayButton, PyDMLabel
from qtpy.QtWidgets import QLabel
import siriushlacommon.data_model

from siriushlacon.mks937b.consts import MKS_MAIN_UI, DEVICE_MENU, DEVICES
from siriushlacon.utils.widgets import get_label, TableDataController, TableDataRow

logger = logging.getLogger("MKS_Logger")


class MKSTableDataController(TableDataController):
    def __init__(
        self,
        table,
        devices: List[siriushlacommon.data_model.Device] = [],
        table_batch: int = 24,
        horizontal_header_labels: List[str] = [],
        *args,
        **kwargs
    ):
        super().__init__(
            table,
            devices=devices,
            table_batch=table_batch,
            horizontal_header_labels=horizontal_header_labels,
            *args,
            **kwargs
        )

    def init_table(self):
        self.table.setRowCount(self.table_batch)
        self.table.setColumnCount(len(self.horizontalHeaderLabels))
        self.table.setHorizontalHeaderLabels(self.horizontalHeaderLabels)
        for actual_row in range(self.table_batch):
            row = 0
            self.table.setCellWidget(actual_row, row, QLabel(""))
            row += 1
            self.table.setCellWidget(actual_row, row, QLabel(""))
            row += 1
            self.table.setCellWidget(actual_row, row, get_label(self.table, "", ""))
            row += 1
            self.table.setCellWidget(actual_row, row, get_label(self.table, "", ""))
            row += 1
            self.table.setCellWidget(actual_row, row, get_label(self.table, "", ""))
            row += 1
            for i in range(13):
                self.table.setCellWidget(actual_row, row, get_label(self.table, "", ""))
                row += 1
            rel = PyDMRelatedDisplayButton(self.table)
            rel.filenames = [DEVICE_MENU]
            rel.openInNewWindow = True
            self.table.setCellWidget(actual_row, row, rel)
            row += 1

    def filter(self, pattern):
        if pattern != self.filter_pattern:
            self.filter_pattern = pattern if pattern is not None else ""
            self.batch_offset = 0
            self.filter_pattern = pattern

            for tableDataRow in self.table_data:
                tableDataRow.render = (
                    self.filter_pattern in tableDataRow.device.prefix
                    or self.filter_pattern in tableDataRow.channel.prefix
                )
            self.update_content.emit()

    def load_table_data(self):
        for device in self.devices:
            if not device.enable:
                continue
            for channel in device.channels:
                if not channel.enable:
                    continue
                self.table_data.append(TableDataRow(device, channel, True))

        self.total_rows = self.table_data.__len__()

        self.update_content.emit()

    def generate_macros(self, dataRow: TableDataRow) -> str:
        macros = {}
        macros["DEVICE"] = dataRow.device.prefix
        for channel in dataRow.device.channels:
            macros["G{}".format(channel.num + 1)] = channel.prefix

            if channel.name == "A1":
                macros["A"] = channel.info.sensor
            if channel.name == "A1":
                macros["B"] = channel.info.sensor
            if channel.name == "C1":
                macros["C"] = channel.info.sensor

        return json.dumps(macros)

    def update_table_row(self, actual_row, dataRow: TableDataRow):
        self.table.setRowHidden(actual_row, False)
        col = 0

        # Channel Access
        device_ca = "ca://" + dataRow.device.prefix
        channel_ca = "ca://" + dataRow.channel.prefix

        self.table.cellWidget(actual_row, col).setText(dataRow.channel.prefix)
        col += 1
        self.table.cellWidget(actual_row, col).setText(dataRow.device.prefix)
        col += 1
        self.connect_widget(actual_row, col, channel_ca + ":Pressure-Mon-s")
        col += 1
        self.connect_widget(actual_row, col, channel_ca + ":Pressure-Mon.STAT")
        col += 1
        self.connect_widget(actual_row, col, device_ca + ":Unit")
        col += 1

        # Setpoint
        self.connect_widget(actual_row, col, channel_ca + ":ProtectionSetpoint-RB-s")
        col += 1
        for i in range(1, 13):
            _pv = ""
            if (
                (dataRow.channel.num == 0 and (1 <= i <= 4))
                or (dataRow.channel.num == 2 and (5 <= i <= 8))
                or (dataRow.channel.num == 3 and (9 <= i <= 10))
                or (dataRow.channel.num == 4 and (11 <= i <= 12))
            ):
                _pv = device_ca + ":Relay{}:Setpoint-RB".format(i)
                self.table.cellWidget(
                    actual_row, col
                ).displayFormat = PyDMLabel.DisplayFormat.Exponential
                self.connect_widget(actual_row, col, _pv)
            else:
                self.connect_widget(actual_row, col, _pv)
                self.table.cellWidget(actual_row, col).displayFormat = 0
                self.table.cellWidget(actual_row, col).value_changed("")

            col += 1

        self.connect_widget(actual_row, col, None, self.generate_macros(dataRow))

    def update_table_content(self):

        # Maximum Allowed
        if self.batch_offset >= self.total_rows:
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

        for d in self.table_data:
            if actual_row == self.table_batch:
                continue

            # To render or not to render  ...
            if d.render and dataset_row >= self.batch_offset:
                self.update_table_row(actual_row, d)
                actual_row += 1

            dataset_row += 1

        for row in range(actual_row, self.table_batch):
            self.table.setRowHidden(row, True)


class MKS(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(MKS, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=MKS_MAIN_UI
        )
        self.caput_lock = threading.RLock()
        self.caput_enable = True

        table_batch = len(DEVICES) * 6
        horizontal_header_labels = [
            "Gauge",
            "Device",
            "Pressure",
            "Alarm",
            "Unit",
            "Protect",
            "Relay 1",
            "Relay 2",
            "Relay 3",
            "Relay 4",
            "Relay 5",
            "Relay 6",
            "Relay 7",
            "Relay 8",
            "Relay 9",
            "Relay 10",
            "Relay 11",
            "Relay 12",
            "Details",
        ]

        self.tdc = MKSTableDataController(
            self.table,
            devices=DEVICES,
            table_batch=table_batch,
            horizontal_header_labels=horizontal_header_labels,
        )

        self.tfFilter.editingFinished.connect(lambda: self.filter(self.tfFilter.text()))

        self.btnNavLeft.clicked.connect(lambda: self.update_navbar(False))
        self.btnNavLeft.setIcon(IconFont().icon("arrow-left"))
        self.btnNavRight.clicked.connect(lambda: self.update_navbar(True))
        self.btnNavRight.setIcon(IconFont().icon("arrow-right"))

        self.btnAllHvOn.clicked.connect(lambda: self.turn_on_channels())

    def turn_on_channels(self):
        with self.caput_lock:
            if self.caput_enable:
                logger.info("Turning all channels ON")
                thread = threading.Thread(target=self.turn_on, daemon=True)
                thread.start()
                self.caput_enable = False
            else:
                logger.info("Wait the previous command completion")

    def turn_on(self):
        for d in DEVICES:
            if not d.enable:
                continue
            for channel in d.channels:
                if not channel.enable:
                    continue

                command = channel.prefix + ":Enable-SP"
                res = epics.caput(command, "On", timeout=0.2)
                logger.info(
                    "Caput command: {} 'On' {}".format(
                        command, "OK" if res == 1 else "FAIL"
                    )
                )
        with self.caput_lock:
            self.caput_enable = True

    def filter(self, pattern):
        self.tdc.filter(pattern)

    def update_navbar(self, increase=True):
        self.tdc.changeBatch(increase)
