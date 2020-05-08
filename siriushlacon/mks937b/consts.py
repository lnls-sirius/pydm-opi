#!/usr/bin/env python3

import pkg_resources


import conscommon.data
from siriushlacon.utils import LazyDevices


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


MKS_OVERVIEW = get_abs_path("overview.py")

MKS_MAIN = get_abs_path("main.py")
MKS_MAIN_UI = get_abs_path("ui/table.ui")

MKS_LAUNCH = get_abs_path("launcher.py")
MKS_LAUNCH_UI = get_abs_path("ui/main.ui")

STORAGE_RING = get_abs_path("storage_ring.py")
STORAGE_RING_UI = get_abs_path("ui/storage_ring.ui")

BOOSTER = get_abs_path("booster.py")
BOOSTER_UI = get_abs_path("ui/booster.ui")

BTS = get_abs_path("bts.py")
BTS_UI = get_abs_path("ui/bts.ui")

LTB = get_abs_path("ltb.py")
LTB_UI = get_abs_path("ui/ltb.ui")

NONE_UI = get_abs_path("ui/mks937b/none.ui")

DEVICE_PREVIEW = get_abs_path("device_preview.py")
DEVICE_PREVIEW_UI = get_abs_path("ui/device_preview.ui")

CC_UI = get_abs_path("ui/cc.ui")

PR_UI = get_abs_path("ui/pirani.ui")

PRESSURE = get_abs_path("pressure.py")
PRESSURE_UI = get_abs_path("ui/pressure.ui")

SETTINGS = get_abs_path("settings.py")
SETTINGS_UI = get_abs_path("ui/settings.ui")

INFO_UI = get_abs_path("ui/info.ui")

DEVICE_MENU = get_abs_path("device_menu.py")
DEVICE_MENU_UI = get_abs_path("ui/device_menu.ui")

IOC_MAN_UI = get_abs_path("ui/ioc_man.ui")

lazy_devices = LazyDevices(conscommon.data.getMKS)
