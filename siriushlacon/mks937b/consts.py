#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pandas

from siriushlacon.utils.consts import FILE

IOC_FILENAME = '/opt/stream-ioc/mks937_min.cmd'


# Consts
def get_abs_path(filename):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)


MKS_OVERVIEW = get_abs_path('overview.py')

MKS_MAIN = get_abs_path('main.py')
MKS_MAIN_UI = get_abs_path('ui/table.ui')

MKS_LAUNCH = get_abs_path('launcher.py')
MKS_LAUNCH_UI = get_abs_path('ui/main.ui')

STORAGE_RING = get_abs_path('storage_ring.py')
STORAGE_RING_UI = get_abs_path('ui/storage_ring.ui')

BOOSTER = get_abs_path('booster.py')
BOOSTER_UI = get_abs_path('ui/booster.ui')

BTS = get_abs_path('bts.py')
BTS_UI = get_abs_path('ui/bts.ui')

LTB = get_abs_path('ltb.py')
LTB_UI = get_abs_path('ui/ltb.ui')

NONE_UI = get_abs_path('ui/mks937b/none.ui')

DEVICE_PREVIEW = get_abs_path('device_preview.py')
DEVICE_PREVIEW_UI = get_abs_path('ui/device_preview.ui')

# CC = get_abs_path('cc.py')
CC_UI = get_abs_path('ui/cc.ui')

# PR = get_abs_path('pirani.py')
PR_UI = get_abs_path('ui/pirani.ui')

PRESSURE = get_abs_path('pressure.py')
PRESSURE_UI = get_abs_path('ui/pressure.ui')

SETTINGS = get_abs_path('settings.py')
SETTINGS_UI = get_abs_path('ui/settings.ui')

# INFO = get_abs_path('info.py')
INFO_UI = get_abs_path('ui/info.ui')

DEVICE_MENU = get_abs_path('device_menu.py')
DEVICE_MENU_UI = get_abs_path('ui/device_menu.ui')

# IOC_MAN = get_abs_path('ioc_man.py')
IOC_MAN_UI = get_abs_path('ui/ioc_man.ui')


# Data and devices
SHEET = 'PVs MKS937b'
sheet = pandas.read_excel(FILE, sheet_name=SHEET, dtype=str)
sheet = sheet.replace('nan', '')
data = []
devices = []

COLD_CATHODE = 'CC'
PIRANI = 'PR'
NONE = 'None'


class DataRow():
    def __init__(self, row):
        self.enable = True if row['ENABLE'] == 'True' else False

        self.channel_config = []
        for config in row['Configuracao'].split(' '):
            self.channel_config.append(
                COLD_CATHODE if config == 'CC' else PIRANI)

        self.channel_prefix = []
        self.channel_prefix.append(row['A1'])
        self.channel_prefix.append(row['A2'])
        self.channel_prefix.append(row['B1'])
        self.channel_prefix.append(row['B2'])
        self.channel_prefix.append(row['C1'])
        self.channel_prefix.append(row['C2'])

        self.device = row['Dispositivo']
        self.ip = row['IP']
        self.sector = row['Setor']
        self.rs485_id = row['RS485 ID']
        self.rack = row['Rack']


# Setor	RS485 ID	Rack	Dispositivo	A1	A2	B1	B2	C1	C2
for index, row in sheet.iterrows():
    data.append(DataRow(row))

    d = [row['Dispositivo']]

    for c in row['Configuracao'].split(' '):
        if c == 'CC':
            d.append(COLD_CATHODE)
        else:
            d.append(PIRANI)

    d.append(row['A1'])
    d.append(row['A2'])
    d.append(row['B1'])
    d.append(row['B2'])
    d.append(row['C1'])
    d.append(row['C2'])

    devices.append(d)
