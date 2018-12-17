#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas
import re

from . import FILE, IS_LINUX

SHEET = 'PVs MKS937b'
sheet = pandas.read_excel(FILE, sheet_name=SHEET, dtype=str)
sheet = sheet.replace('nan', '')

COLD_CATHODE = 'CC'
PIRANI = 'PR'
NONE = 'None'

IOC_FILENAME = '/opt/stream-ioc/' + 'mks937_min.cmd'

devices = []
# Setor	RS485 ID	Rack	Dispositivo	A1	A2	B1	B2	C1	C2
for index, row in sheet.iterrows():
    data = [row['Dispositivo']]

    for c in  row['Configuracao'].split(' '):
        if c == 'CC':
            data.append(COLD_CATHODE)
        else:
            data.append(PIRANI)

    data.append(row['A1'])
    data.append(row['A2'])
    data.append(row['B1'])
    data.append(row['B2'])
    data.append(row['C1'])
    data.append(row['C2'])

    devices.append(data)