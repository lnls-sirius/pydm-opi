#!/usr/bin/python3
import epics
import os
import pandas

def set_mks_channel_on():
    spreadsheet = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../../Redes e Beaglebones.xlsx')

    sheet = pandas.read_excel(spreadsheet, sheet_name='PVs MKS937b', dtype=str)
    sheet = sheet.replace('nan', '')

    for index, row in sheet.iterrows():
        epics.caput(row['A1'] +':Enable-SP', 1)
        epics.caput(row['A2'] +':Enable-SP', 1)
        epics.caput(row['B1'] +':Enable-SP', 1)
        epics.caput(row['B2'] +':Enable-SP', 1)
        epics.caput(row['C1'] +':Enable-SP', 1)
        epics.caput(row['C2'] +':Enable-SP', 1)



if __name__ == '__main__':
    set_mks_channel_on()
