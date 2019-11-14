#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pkg_resources

def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


DATA_JSON = get_abs_path('data.json')
REGATRON_MAIN = get_abs_path('main.py')
ERR_MAIN = get_abs_path('err.py')
WARN_MAIN = get_abs_path('warn.py')
COMPLETE_MAIN = get_abs_path('regatron.py')
ALARM_MAIN = get_abs_path('alarm.py')

REGATRON_UI = get_abs_path('ui/main.ui')
ERR_UI = get_abs_path('ui/err.ui')
WARN_UI = get_abs_path('ui/warning.ui')
COMPLETE_UI = get_abs_path('ui/regatron.ui')
ALARM_UI = get_abs_path('ui/alarm.ui')

EXTENDED_MAP = {
    0: 'IBC System',    1: 'IBC Supply',        2: 'IBC Communication', 3: 'IBC Power',
    4: 'IBC Inverter',  5: 'IBC Miscellaneous', 6: 'IBC Inverter 2',    7: 'not used',
    8: 'not used',      9: 'not used',          10: 'Supply 2',         11:'Login 2',
    12: 'Configuration 3',   13: 'Communication 3',
    14: 'Internal 2', 15:'Communication 2'
}
STANDARD_MAP = {
    0: 'Internal', 1: 'Internal (PDSP)',  2: 'Output Current',   3: 'Output Voltage',
    4: 'Supply',   5: 'Temperature',      6: 'Communication',    7: 'Internal (Modulator)',
    8: 'Internal (AD overrange 1)',      9: 'Internal (AD overrange 2)',
    10: 'Internal (AD underrange 1)',    11: 'Internal (AD underrange 2)',
    12: 'Login',   13: 'Configuration',   14: 'Configuration 2', 15: 'Miscellaneous'
}

STD_READINGS = [
    "Intrn-Mon",
    "IntrnPDSP-Mon",
    "OutCurrent-Mon",
    "OutVolt-Mon",
    "Supply-Mon",
    "T-Mon",
    "Comm-Mon",
    "IntrnMod-Mon",
    "AD1Ovr-Mon",
    "AD2Ovr-Mon",
    "AD1Undr-Mon",
    "AD2Undr-Mon",
    "Login-Mon",
    "Conf-Mon",
    "Conf2-Mon",
    "Misc-Mon",
]

EXT_READINGS = [
    "IBCSystem-Mon",
    "IBCSuppply-Mon",
    "IBCComm-Mon",
    "IBCPwr-Mon1",
    "IBCInv-Mon",
    "IBCMisc-Mon",
    "IBCInv2-Mon",
    "Supply2-Mon",
    "Login2-Mon",
    "Conf3-Mon",
    "Comm3-Mon",
    "Intrn2-Mon",
    "Comm2-Mon"
]
