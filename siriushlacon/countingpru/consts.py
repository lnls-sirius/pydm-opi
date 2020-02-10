#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pkg_resources


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)

GAMMA_COUNTING_MAIN = get_abs_path('main.py')
GAMMA_COUNTING_MAIN_UI = get_abs_path('ui/main.ui')

OVERVIEW_UI = get_abs_path('ui/overview.ui')
LAYOUT_OVERVIEW_UI = get_abs_path('ui/layout_overview.ui')

BEFORE_BC_IMAGE = get_abs_path('pic/BeforeBC.png')
AFTER_BC_IMAGE = get_abs_path('pic/AfterBC.png')
LNLS_IMAGE = get_abs_path('pic/lnlsLogo.png')
CNPEM_IMAGE = get_abs_path('pic/CNPEM.png')
