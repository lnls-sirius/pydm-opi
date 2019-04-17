#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas
import re

from . import FILE

SHEET = 'PVs Agilent 4UHV'
sheet = pandas.read_excel(FILE, sheet_name=SHEET, dtype=str)
sheet = sheet.replace('nan', '')

devices = []

data = []
class DataRow():
    def __init__(self, row):
        self.enable = True if row['ENABLE'] == 'True' else False

        self.channel_prefix = []
        self.channel_prefix.append(row['C1'])
        self.channel_prefix.append(row['C2'])
        self.channel_prefix.append(row['C3'])
        self.channel_prefix.append(row['C4'])

        self.ip         = row['IP']
        self.sector     = row['Setor']
        self.rs485_id   = row['RS485 ID']
        self.rack       = row['Rack']
        
# Setor	RS485 ID	Rack	Dispositivo	C1	C2	C3	C4
for index, row in sheet.iterrows():
    data.append(DataRow(row))
    
    setor = row['Setor']
    d = [row['Dispositivo'], row['C1'], row['C2'], row['C3'], row['C4']]
    devices.append(d)
