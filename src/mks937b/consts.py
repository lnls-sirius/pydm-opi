#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import re 
import pandas

FILE = os.path.dirname(os.path.realpath(__file__)) + '/../../etc/devices.xlsx'
SHEET = 'PVs MKS937b'

sheet = pandas.read_excel(FILE, sheet_name=SHEET, dtype=str) 
sheet = sheet.replace('nan', '')

IS_LINUX = (os.name == 'posix' or platform.system() == 'Linux')

COLD_CATHODE = 'CC'
PIRANI = 'PR'
NONE = 'None'

IOC_FILENAME = '/opt/stream-ioc/' + 'mks937_min.cmd'
ARCHIVER_URL = 'https://10.0.6.57/mgmt/ui/index.html'


DEVICE_PREFIX = ""
ARGS_HIDE_ALL = ['--hide-nav-bar', '--hide-menu-bar', '--hide-status-bar']

ring_sub_sectors = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
ring_sector_devices = []

booster_sub_sectors = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
booster_sector_devices = []

ltb_sub_sectors = ['1']
ltb_sector_devices = []

bts_sub_sectors = ['1']
bts_sector_devices = []

# Setor	RS485 ID	Rack	Dispositivo	A1	A2	B1	B2	C1	C2
for index, row in sheet.iterrows():
    setor = row['Setor']
    data = [row['Dispositivo']]

    for c in  row['Configuracao'].split(' '):
        if c == 'CC':
            data.append(COLD_CATHODE)
        else:
            data.append(PIRANI)
    
    data.append([row['A1'], row['A2'], row['B1'], row['B2'], row['C1'], row['C2']])
    
    if setor == 'Booster':
        booster_sector_devices.append(data)
    elif setor == 'Anel':
        ring_sector_devices.append(data)
    elif setor == 'BTS':
        bts_sector_devices.append(data)
    elif setor == 'LTB':
        ltb_sector_devices.append(data)