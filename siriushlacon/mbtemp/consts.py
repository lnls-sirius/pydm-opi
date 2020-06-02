#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import pkg_resources

import conscommon.data

from siriushlacon.utils import LazyDevices

logger = logging.getLogger()

def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)

MBTEMP_MAIN        = get_abs_path("main.py")
MBTEMP_MAIN_UI     = get_abs_path('ui/main.ui')

OVERVIEW_MAIN      = get_abs_path("overview/main.py")
OVERVIEW_MAIN_UI   = get_abs_path("overview/ui/main.ui")

LNLS_LOGO          = get_abs_path('pic/lnls-logo.png')
CNPEM_LOGO         = get_abs_path('pic/cnpem-logo.png')
BOEXTRACTION_PIC   = get_abs_path('pic/TL/BOExtraction.png')
SRINJ_PIC          = get_abs_path('pic/TL/SRInj.png')
BOINJ_PIC          = get_abs_path('pic/TL/BOInj.png')

BO_PIC1            = get_abs_path('pic/BO/Booster1.png')
BO_PIC2            = get_abs_path('pic/BO/Booster2.png')
BO_PIC3            = get_abs_path('pic/BO/Booster3.png')
BO_PIC4            = get_abs_path('pic/BO/Booster4.png')

SR_PIC1            = get_abs_path('pic/SR/SR_pic1.png')
SR_PIC2            = get_abs_path('pic/SR/SR_pic2.png')
SR_PIC3            = get_abs_path('pic/SR/SR_pic3.png')
SR_PIC4            = get_abs_path('pic/SR/SR_pic4.png')
SR_PIC5            = get_abs_path('pic/SR/SR_pic5.png')
SR_PIC6            = get_abs_path('pic/SR/SR_pic6.png')
SR_PIC7            = get_abs_path('pic/SR/SR_pic7.png')

CHS_MBTEMP         = get_abs_path('channels.xlsx')
PIC_PA             = get_abs_path('pic/Area/PA.jpg')
PIC_LA             = get_abs_path('pic/Area/LA.png')

lazy_devices       = LazyDevices(conscommon.data.getMBTemp)
