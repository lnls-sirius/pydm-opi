#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pkg_resources

def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)

PCTRL_MAIN = get_abs_path('main.py')
PCTRL_UI = get_abs_path('ui/main.ui')
PCTRL_DET_UI = get_abs_path('ui/procServControl.ui')
IOCS_JSON =  get_abs_path('iocs.json')
