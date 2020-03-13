#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pkg_resources

def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)

BEAGLEBONES_MAIN = get_abs_path('main.py')
BEAGLEBONES_MAIN_UI = get_abs_path('ui/main.ui')

INFO_BBB_UI = get_abs_path('ui/info_bbb.ui')
CHANGE_BBB_UI = get_abs_path('ui/change_bbb.ui')
