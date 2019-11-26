#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas
import pkg_resources

from siriushlacon.utils.consts import FILE


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)

AGILENT_OVERVIEW = get_abs_path('overview.py')

AGILENT_MAIN = get_abs_path('main.py')
AGILENT_MAIN_UI = get_abs_path('ui/main.ui')

AGILENT_DEVICE_MAIN = get_abs_path('device_main.py')
AGILENT_DEVICE_MAIN_UI = get_abs_path('ui/device_main.ui')

AGILENT_DEVICE = get_abs_path('device.py')
AGILENT_DEVICE_UI = get_abs_path('ui/device.ui')

AGILENT_CHANNEL = get_abs_path('channel.py')
AGILENT_CHANNEL_UI = get_abs_path('ui/channel.ui')


# Data and devices
SHEET = 'PVs Agilent 4UHV'
sheet = pandas.read_excel(FILE, sheet_name=SHEET, dtype=str)
sheet = sheet.replace('nan', '')

data = []
devices = []


class DataRow():
    def __init__(self, row):
        self.enable = True if row['ENABLE'] == 'True' else False

        self.channel_prefix = []
        self.channel_prefix.append(row['C1'])
        self.channel_prefix.append(row['C2'])
        self.channel_prefix.append(row['C3'])
        self.channel_prefix.append(row['C4'])

        self.ip = row['IP']
        self.sector = row['Setor']
        self.rs485_id = row['RS485 ID']
        self.rack = row['Rack']


# Setor	RS485 ID	Rack	Dispositivo	C1	C2	C3	C4
for index, row in sheet.iterrows():
    data.append(DataRow(row))

    setor = row['Setor']
    d = [row['Dispositivo'], row['C1'], row['C2'], row['C3'], row['C4']]
    devices.append(d)
