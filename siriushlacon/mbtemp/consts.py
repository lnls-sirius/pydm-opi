#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import pkg_resources

import conscommon.data

from siriushlacon.utils import LazyDevices

logger = logging.getLogger()


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


MBTEMP_MAIN = get_abs_path("main.py")
MBTEMP_MAIN_UI = get_abs_path("ui/main.ui")

OVERVIEW_MAIN = get_abs_path("overview.py")
OVERVIEW_MAIN_UI = get_abs_path("ui/overview.ui")

BOEXTRACTION_PIC = get_abs_path("images/TL/BOExtraction.png")
BOINJ_PIC = get_abs_path("images/TL/BOInj.png")

BO_PIC1 = get_abs_path("images/BO/Booster1.png")
BO_PIC2 = get_abs_path("images/BO/Booster2.png")
BO_PIC3 = get_abs_path("images/BO/Booster3.png")
BO_PIC4 = get_abs_path("images/BO/Booster4.png")

CNPEM_LOGO = get_abs_path("images/cnpem-logo.png")
LNLS_LOGO = get_abs_path("images/lnls-logo.png")
SRINJ_PIC = get_abs_path("images/TL/SRInj.png")

SR_PIC1 = get_abs_path("images/SR/SR_pic1.png")
SR_PIC2 = get_abs_path("images/SR/SR_pic2.png")
SR_PIC3 = get_abs_path("images/SR/SR_pic3.png")
SR_PIC4 = get_abs_path("images/SR/SR_pic4.png")
SR_PIC5 = get_abs_path("images/SR/SR_pic5.png")
SR_PIC6 = get_abs_path("images/SR/SR_pic6.png")
SR_PIC7 = get_abs_path("images/SR/SR_pic7.png")
SR_PICS = {
    1: SR_PIC1,
    2: SR_PIC2,
    3: SR_PIC3,
    4: SR_PIC4,
    5: SR_PIC5,
    6: SR_PIC6,
    7: SR_PIC7,
}

PIC_PA = get_abs_path("images/Area/PA.jpg")
PIC_LA = get_abs_path("images/Area/LA.png")

PIC_P7RF = get_abs_path("images/Area/Petra7.png")

lazy_devices = LazyDevices(conscommon.data.getMBTemp)
