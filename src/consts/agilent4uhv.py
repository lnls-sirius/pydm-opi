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

# Setor	RS485 ID	Rack	Dispositivo	C1	C2	C3	C4
for index, row in sheet.iterrows():
    setor = row['Setor']
    data = [row['Dispositivo'], row['C1'], row['C2'], row['C3'], row['C4']]
    devices.append(data)
