#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pkg_resources

def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)

DATA_JSON = get_abs_path('data.json')

REGATRON_MAIN = get_abs_path('main.py')
DETAILS_MAIN = get_abs_path('details.py')
SIMPLE_MAIN = get_abs_path('simple.py')
ERR_MAIN = get_abs_path('err.py')
WARN_MAIN = get_abs_path('warn.py')

REGATRON_UI = get_abs_path('ui/main.ui')
DETAILS_UI = get_abs_path('ui/details.ui')
SIMPLE_UI = get_abs_path('ui/simple.ui')
ERR_UI = get_abs_path('ui/err.ui')
WARN_UI = get_abs_path('ui/warning.ui')

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
    "IBCInverter-Mon",
    "IBCMisc-Mon",
    "IBCInverter2-Mon",
    "Supply2-Mon",
    "Login2-Mon",
    "Conf3-Mon",
    "Comm3-Mon",
    "Intrn2-Mon",
    "Comm2-Mon"
]
