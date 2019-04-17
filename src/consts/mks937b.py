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

class DataRow():
    def __init__(self, row):
        self.enable = True if row['ENABLE'] == 'True' else False
        
        self.channel_config = []
        for config in row['Configuracao'].split(' '):
            self.channel_config.append(COLD_CATHODE if config == 'CC' else PIRANI)
        
        self.channel_prefix = []
        self.channel_prefix.append(row['A1'])
        self.channel_prefix.append(row['A2'])
        self.channel_prefix.append(row['B1'])
        self.channel_prefix.append(row['B2'])
        self.channel_prefix.append(row['C1'])
        self.channel_prefix.append(row['C2'])

        self.ip         = row['IP']
        self.sector     = row['Setor']
        self.rs485_id   = row['RS485 ID']
        self.rack       = row['Rack']


data = []
devices = []
# Setor	RS485 ID	Rack	Dispositivo	A1	A2	B1	B2	C1	C2
for index, row in sheet.iterrows():
    data.append(DataRow(row))

    d = [row['Dispositivo']]

    for c in  row['Configuracao'].split(' '):
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