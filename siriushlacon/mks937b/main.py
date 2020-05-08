#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import enum
import json
import logging
import re
import threading
from typing import List

from qtpy.QtWidgets import QLabel, QCheckBox
from qtpy.QtCore import Qt
from pydm import Display
from pydm.utilities import IconFont
from pydm.widgets import PyDMRelatedDisplayButton, PyDMLabel
import conscommon.data_model

from siriushlacon.mks937b.consts import MKS_MAIN_UI, DEVICE_MENU, lazy_devices
from siriushlacon.utils.widgets import get_label, TableDataController, TableDataRow

CH_REG = re.compile(r":[ABC][0-9]")
DEVICES = lazy_devices.get()

logger = logging.getLogger()


@enum.unique
class TableColumn(enum.Enum):
    # fmt: off
    Channel       = "Channel"
    Device        = "Device"
    Pressure      = "Pressure"
    Alarm         = "Alarm"
    Unit          = "Unit"
    Protect       = "Protect"
    Relay_1_SP    = "Relay 1 SP"
    Relay_1_Hyst  = "Relay 1 Hyst"
    Relay_5_SP    = "Relay 5 SP"
    Relay_5_Hyst  = "Relay 5 Hyst"
    Relay_7_SP    = "Relay 7 SP"
    Relay_7_Hyst  = "Relay 7 Hyst"
    Relay_11_SP   = "Relay 11 SP"
    Relay_11_Hyst = "Relay 11 Hyst"
    Relay_12_SP   = "Relay 12 SP"
    Relay_12_Hyst = "Relay 12 Hyst"
    Details       = "Details"
    # fmt: on


class MKSTableDataController(TableDataController):
    def __init__(
        self,
        table,
        devices: List[conscommon.data_model.Device] = [],
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
            col = 0
            for col_name in TableColumn:
                if col_name in [TableColumn.Device, TableColumn.Channel]:
                    self.table.setCellWidget(actual_row, col, QLabel(""))

                elif col_name == TableColumn.Details:
                    rel = PyDMRelatedDisplayButton(self.table)
                    rel.filenames = [DEVICE_MENU]
                    rel.openInNewWindow = True
                    self.table.setCellWidget(actual_row, col, rel)
                    rel.show()
                else:
                    self.table.setCellWidget(
                        actual_row, col, get_label(self.table, showUnits=False)
                    )
                col += 1

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
                if not channel.enable or CH_REG.match(channel.prefix[-3:]):
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

    def getRelayPV(self, col_name, channel: conscommon.data_model.Channel):
        if "Relay" not in col_name:
            return ""

        _data = col_name.split(" ")
        _relay_num = _data[1]
        _t = _data[2]
        sufix = "Hyst-RB" if _t == "Hyst" else "Setpoint-RB"
        if (
            (channel.num == 0 and _relay_num == "1")
            or (channel.num == 2 and _relay_num in ["5", "7"])
            or (channel.num in [4, 5] and _relay_num in ["11", "12"])
        ):
            return ":Relay{}:{}".format(_relay_num, sufix)
        else:
            return ""

    def update_table_row(self, actual_row, dataRow: TableDataRow):
        self.table.setRowHidden(actual_row, False)
        col = 0
        # Channel Access
        device_ca = "ca://" + dataRow.device.prefix
        channel_ca = "ca://" + dataRow.channel.prefix
        for tc in TableColumn:
            if tc == TableColumn.Device:
                self.table.cellWidget(actual_row, col).setText(dataRow.device.prefix)
            elif tc == TableColumn.Channel:
                self.table.cellWidget(actual_row, col).setText(dataRow.channel.prefix)
            elif tc == TableColumn.Pressure:
                self.connect_widget(actual_row, col, channel_ca + ":Pressure-Mon-s")
            elif tc == TableColumn.Alarm:
                self.connect_widget(actual_row, col, channel_ca + ":Pressure-Mon.STAT")
            elif tc == TableColumn.Unit:
                self.connect_widget(actual_row, col, device_ca + ":Unit")
            elif tc == TableColumn.Protect:
                self.connect_widget(
                    actual_row, col, channel_ca + ":ProtectionSetpoint-RB-s"
                )
            elif tc == TableColumn.Details:
                self.connect_widget(
                    actual_row, col, None, self.generate_macros(dataRow)
                )
            else:
                _pv = self.getRelayPV(tc.value, dataRow.channel)
                if _pv != "":
                    self.table.cellWidget(
                        actual_row, col
                    ).displayFormat = PyDMLabel.DisplayFormat.Exponential
                    self.connect_widget(actual_row, col, device_ca + _pv)
                else:
                    self.connect_widget(actual_row, col, _pv)
                    self.table.cellWidget(actual_row, col).displayFormat = 0
                    self.table.cellWidget(actual_row, col).value_changed("")

            col += 1

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

        table_batch = 0
        for device in DEVICES:
            if not device.enable:
                continue
            for channel in device.channels:
                if not channel.enable or CH_REG.match(channel.prefix[-3:]):
                    continue
                table_batch += 1

        horizontal_header_labels = [tc.value for tc in TableColumn]
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

        self.checkBoxAlarm: QCheckBox
        self.checkBoxUnit: QCheckBox
        self.checkBoxProtect: QCheckBox
        self.checkBoxRelay1: QCheckBox
        self.checkBoxRelay5: QCheckBox
        self.checkBoxRelay7: QCheckBox
        self.checkBoxRelayPirani: QCheckBox

        self.checkBoxAlarm.stateChanged.connect(self.displayColumns)
        self.checkBoxUnit.stateChanged.connect(self.displayColumns)
        self.checkBoxProtect.stateChanged.connect(self.displayColumns)
        self.checkBoxRelay1.stateChanged.connect(self.displayColumns)
        self.checkBoxRelay5.stateChanged.connect(self.displayColumns)
        self.checkBoxRelay7.stateChanged.connect(self.displayColumns)
        self.checkBoxRelayPirani.stateChanged.connect(self.displayColumns)

        self.checkBoxAlarm.setCheckState(2)
        self.checkBoxUnit.setCheckState(2)
        self.checkBoxProtect.setCheckState(2)
        self.checkBoxRelay1.setCheckState(0)
        self.checkBoxRelay5.setCheckState(0)
        self.checkBoxRelay7.setCheckState(0)
        self.checkBoxRelayPirani.setCheckState(0)

        for i in range(6, 16):
            self.table.setColumnHidden(i, True)

    def displayColumns(self, *args, **kwargs):
        # fmt: off
        self.table.setColumnHidden(3, self.checkBoxAlarm.checkState() != Qt.Checked)
        self.table.setColumnHidden(4, self.checkBoxUnit.checkState() != Qt.Checked)
        self.table.setColumnHidden(5, self.checkBoxProtect.checkState() != Qt.Checked)

        self.table.setColumnHidden(6, self.checkBoxRelay1.checkState() != Qt.Checked)
        self.table.setColumnHidden(7, self.checkBoxRelay1.checkState() != Qt.Checked)

        self.table.setColumnHidden(8, self.checkBoxRelay5.checkState() != Qt.Checked)
        self.table.setColumnHidden(9, self.checkBoxRelay5.checkState() != Qt.Checked)
        self.table.setColumnHidden(10, self.checkBoxRelay7.checkState() != Qt.Checked)
        self.table.setColumnHidden(11, self.checkBoxRelay7.checkState() != Qt.Checked)

        self.table.setColumnHidden(12, self.checkBoxRelayPirani.checkState() != Qt.Checked)
        self.table.setColumnHidden(13, self.checkBoxRelayPirani.checkState() != Qt.Checked)
        self.table.setColumnHidden(14, self.checkBoxRelayPirani.checkState() != Qt.Checked)
        self.table.setColumnHidden(15, self.checkBoxRelayPirani.checkState() != Qt.Checked)
        # fmt: on

    def filter(self, pattern):
        self.tdc.filter(pattern)

    def update_navbar(self, increase=True):
        self.tdc.changeBatch(increase)
