#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import re 
import pandas

FILE = os.path.dirname(os.path.realpath(__file__)) + '/../../etc/devices.xlsx'
SHEET = 'PVs Agilent 4UHV'

sheet = pandas.read_excel(FILE, sheet_name=SHEET, dtype=str) 
sheet = sheet.replace('nan', '')

ring_sub_sectors = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
ring_sector_devices = []

booster_sub_sectors = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
booster_sector_devices = []

ltb_sub_sectors = ['1']
ltb_sector_devices = []

bts_sub_sectors = ['1']
bts_sector_devices = []

# Setor	RS485 ID	Rack	Dispositivo	C1	C2	C3	C4
for index, row in sheet.iterrows():
    setor = row['Setor']
    data = [row['Dispositivo'], row['C1'], row['C2'], row['C3'], row['C4']]

    if setor == 'Booster':
        booster_sector_devices.append(data)
    elif setor == 'Anel':
        ring_sector_devices.append(data)
    elif setor == 'BTS':
        bts_sector_devices.append(data)
    elif setor == 'LTB':
        ltb_sector_devices.append(data)
