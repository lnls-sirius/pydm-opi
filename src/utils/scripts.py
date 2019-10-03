#!/usr/bin/python3
import epics
import pandas
from src.utils.consts import FILE


def set_mks_channel_on():
    sheet = pandas.read_excel(FILE, sheet_name='PVs MKS937b', dtype=str)
    sheet = sheet.replace('nan', '')

    for index, row in sheet.iterrows():
        epics.caput(row['A1'] + ':Enable-SP', 1)
        epics.caput(row['A2'] + ':Enable-SP', 1)
        epics.caput(row['B1'] + ':Enable-SP', 1)
        epics.caput(row['B2'] + ':Enable-SP', 1)
        epics.caput(row['C1'] + ':Enable-SP', 1)
        epics.caput(row['C2'] + ':Enable-SP', 1)


if __name__ == '__main__':
    set_mks_channel_on()
