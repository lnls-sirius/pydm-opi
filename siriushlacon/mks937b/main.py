#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import threading

import epics
from pydm import Display
from pydm.utilities import IconFont
from pydm.widgets import PyDMRelatedDisplayButton, PyDMLabel
from qtpy.QtWidgets import QLabel

from siriushlacon.mks937b.consts import devices, data, MKS_MAIN_UI, DEVICE_MENU
from siriushlacon.utils.widgets import get_label, TableDataController

logger = logging.getLogger('MKS_Logger')


class MKSTableDataController(TableDataController):

    def __init__(self, table, devices=[], table_batch=24,
                 horizontal_header_labels=[], *args, **kwargs):
        super().__init__(
            table,
            devices=devices,
            table_batch=table_batch,
            horizontal_header_labels=horizontal_header_labels,
            *args, **kwargs)

    def init_table(self):
        self.table.setRowCount(self.table_batch)
        self.table.setColumnCount(len(self.horizontalHeaderLabels))
        self.table.setHorizontalHeaderLabels(self.horizontalHeaderLabels)
        for actual_row in range(self.table_batch):
            row = 0
            self.table.setCellWidget(actual_row, row, QLabel(''))
            row += 1
            self.table.setCellWidget(actual_row, row, QLabel(''))
            row += 1
            self.table.setCellWidget(actual_row, row, get_label(
                self.table, '', ''))
            row += 1
            self.table.setCellWidget(actual_row, row, get_label(
                self.table, '', ''))
            row += 1
            self.table.setCellWidget(actual_row, row, get_label(
                self.table, '', ''))
            row += 1
            for i in range(13):
                self.table.setCellWidget(actual_row, row, get_label(
                    self.table, '', ''))
                row += 1
            rel = PyDMRelatedDisplayButton(self.table)
            rel.filenames = [DEVICE_MENU]
            rel.openInNewWindow = True
            self.table.setCellWidget(actual_row, row, rel)
            row += 1

    def filter(self, pattern):
        if pattern != self.filter_pattern:
            self.filter_pattern = pattern if pattern is not None else ''
            self.batch_offset = 0
            self.filter_pattern = pattern

            for d in self.table_data:
                d['render'] = self.filter_pattern in d['device'] or \
                              self.filter_pattern in d['gauge']
            self.update_content.emit()

    def load_table_data(self):
        self.table_data = []
        for device in self.devices:
            # Gauges are from data[4:]
            # Device is data[0]
            macro = \
                '{"DEVICE" :"' + device[0] + '",\
                "G1":"' + device[4] + '",\
                "G2":"' + device[5] + '",\
                "G3":"' + device[6] + '",\
                "G4":"' + device[7] + '",\
                "G5":"' + device[8] + '",\
                "G6":"' + device[9] + '",\
                "A":"' + device[1] + '",\
                "B":"' + device[2] + '", \
                "C":"' + device[3] + '"}'
            i = 0
            for item in device[4:]:
                self.table_data.append({
                    'device': device[0],
                    'gauge': item, 'macro': macro,
                    'render': True, 'num': i})
                i += 1
        self.total_rows = len(self.table_data)
        self.update_content.emit()

    def update_table_content(self):

        # Maximum Allowed
        if self.batch_offset >= self.total_rows:
            return

        # Adding New Content
        actual_row = 0
        dataset_row = 0
        iterable = range(self.batch_offset,
                         self.table_batch + self.batch_offset)
        self.table.setVerticalHeaderLabels([str(i) for i in iterable])

        for d in self.table_data:
            if actual_row == self.table_batch:
                continue

            # To render or not to render  ...
            if d['render'] and dataset_row >= self.batch_offset:
                self.table.setRowHidden(actual_row, False)
                row = 0
                # Channel Access
                device_ca = 'ca://' + d['device']
                channel_ca = 'ca://' + d['gauge']

                self.table.cellWidget(actual_row, row).setText(d['gauge'])
                row += 1
                self.table.cellWidget(actual_row, row).setText(d['device'])
                row += 1
                self.connect_widget(actual_row, row, channel_ca + ':Pressure-Mon-s')
                row += 1
                self.connect_widget(actual_row, row, channel_ca + ':Pressure-Mon.STAT')
                row += 1
                self.connect_widget(actual_row, row, device_ca + ':Unit')
                row += 1

                # Setpoint
                self.connect_widget(actual_row, row, channel_ca + ':ProtectionSetpoint-RB-s')
                row += 1
                for i in range(1, 13):
                    if (d['num'] == 0 and (1 <= i <= 4)) or \
                            (d['num'] == 2 and (5 <= i <= 8)) or \
                            (d['num'] == 3 and (9 <= i <= 10)) or \
                            (d['num'] == 4 and (11 <= i <= 12)):
                        pv_ = device_ca + ':Relay{}:Setpoint-RB'.format(i)
                        self.table.cellWidget(actual_row, row).displayFormat = PyDMLabel.DisplayFormat.Exponential
                        self.connect_widget(actual_row, row, pv_)
                    else:
                        pv_ = ''
                        self.connect_widget(actual_row, row, pv_)
                        self.table.cellWidget(actual_row, row).displayFormat = 0  # PyDMLabel.DisplayFormat.String
                        self.table.cellWidget(actual_row, row).value_changed('')  # setText('')
                    row += 1

                self.connect_widget(actual_row, row, None, d['macro'])
                actual_row += 1

            dataset_row += 1

        for row in range(actual_row, self.table_batch):
            self.table.setRowHidden(row, True)


class MKS(Display):

    def __init__(self, parent=None, args=[], macros=None):
        super(MKS, self).__init__(
            parent=parent, args=args, macros=macros)
        self.caput_lock = threading.RLock()
        self.caput_enable = True

        table_batch = len(devices) * 6
        horizontal_header_labels = [
            'Gauge',
            'Device',
            'Pressure',
            'Alarm',
            'Unit',
            'Protect  SP',
            'Relay 1  SP',
            'Relay 2  SP',
            'Relay 3  SP',
            'Relay 4  SP',
            'Relay 5  SP',
            'Relay 6  SP',
            'Relay 7  SP',
            'Relay 8  SP',
            'Relay 9  SP',
            'Relay 10 SP',
            'Relay 11 SP',
            'Relay 12 SP',
            'Details']

        self.tdc = MKSTableDataController(
            self.table,
            devices=devices,
            table_batch=table_batch,
            horizontal_header_labels=horizontal_header_labels)

        self.tfFilter.editingFinished.connect(
            lambda: self.filter(self.tfFilter.text()))

        self.btnNavLeft.clicked.connect(lambda: self.update_navbar(False))
        self.btnNavLeft.setIcon(IconFont().icon('arrow-left'))
        self.btnNavRight.clicked.connect(lambda: self.update_navbar(True))
        self.btnNavRight.setIcon(IconFont().icon('arrow-right'))

        self.btnAllHvOn.clicked.connect(lambda: self.turn_on_channels())

    def turn_on_channels(self):
        # TODO: use asyncio
        with self.caput_lock:
            if self.caput_enable:
                logger.info('Turning all channels ON')
                thread = threading.Thread(target=self.turn_on, daemon=True)
                thread.start()
                self.caput_enable = False
            else:
                logger.info('Wait the previous command completion')

    def turn_on(self):
        for d in data:
            if not d.enable:
                continue
            for p in d.channel_prefix:
                command = p + ':Enable-SP'
                res = epics.caput(command, 'On', timeout=.2)
                logger.info('Caput command: {} \'On\'         {}'.format(
                    command, 'OK' if res == 1 else 'FAIL'))
        with self.caput_lock:
            self.caput_enable = True

    def filter(self, pattern):
        self.tdc.filter(pattern)

    def update_navbar(self, increase=True):
        self.tdc.changeBatch(increase)

    def ui_filename(self):
        return MKS_MAIN_UI

    def ui_filepath(self):
        return MKS_MAIN_UI
