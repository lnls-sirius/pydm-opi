#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import pandas
import re

from . import FILE, IS_LINUX

SHEET = 'PVs MBTemp'

sheet = pandas.read_excel(FILE, sheet_name=SHEET, dtype=str)
sheet = sheet.replace('nan', '')

IOC_FILENAME = '/opt/stream-ioc/' + 'mks937_min.cmd'
devices = []

#IP	Rack	ADDR	Dev	CH1	CH2	CH3	CH4	CH5	CH6	CH7	CH8
for index, row in sheet.iterrows():
    data = [
        row['Dev'],
        row['CH1'], row['CH2'], row['CH3'],
        row['CH4'], row['CH5'], row['CH6'],
        row['CH7'], row['CH8']
    ]
    devices.append(data)
