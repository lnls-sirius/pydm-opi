#!/usr/bin/python3
import os
import platform

IS_LINUX = (os.name == 'posix' or platform.system() == 'Linux')

def get_abs_path(relative):
    """
    relative = relative path with base at python/
    """
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), relative)

 
LAUNCH_WINDOW_UI = "../ui/launcher.ui"

#######################################################################################
#                                       MBTemp                                        # 
#######################################################################################
MBTEMP_MAIN_UI = '../ui/mbtemp/main.ui'
MBTEMP_MAIN = 'mbtemp.py'

#######################################################################################
#                                      Agilent                                        # 
#######################################################################################
AGILENT_MAIN = "agilent4uhv.py"
AGILENT_MAIN_UI = "../ui/agilent4uhv/main.ui"

# AGILENT_DEVICE_MAIN = "agilent4uhv/device_main.py"
AGILENT_DEVICE_MAIN_UI = "../ui/agilent4uhv/device_main.ui"

#######################################################################################
#                                          MKS                                        # 
#######################################################################################
MKS_MAIN = "mks937b/table.py"
MKS_MAIN_UI = "../ui/mks937b/table.ui"

TABLE = 'mks937b/table.py'
TABLE_UI = '../ui/mks937b/table.ui'

STORAGE_RING = 'mks937b/storage_ring.py'
STORAGE_RING_UI = '../ui/mks937b/storage_ring.ui'

BOOSTER = 'mks937b/booster.py'
BOOSTER_UI = '../ui/mks937b/booster.ui'

BTS = 'mks937b/bts.py'
BTS_UI = '../ui/mks937b/bts.ui'

LTB = 'mks937b/ltb.py'
LTB_UI = '../ui/mks937b/ltb.ui'

NONE_UI = '../ui/mks937b/none.ui'

DEVICE_PREVIEW = 'mks937b/device_preview.py'
DEVICE_PREVIEW_UI = '../ui/mks937b/device_preview.ui'

CC = 'mks937b/cc.py'
CC_UI = '../ui/mks937b/cc.ui'

PR = 'mks937b/pirani.py'
PR_UI = '../ui/mks937b/pirani.ui'

PRESSURE = 'mks937b/pressure.py'
if IS_LINUX:
    PRESSURE_UI = '../ui/mks937b/pressure.ui'
else:
    PRESSURE_UI = '../ui/mks937b/pressure_win.ui'

SETTINGS = 'mks937b/settings.py'
SETTINGS_UI = '../ui/mks937b/settings.ui'

INFO = 'mks937b/info.py'
INFO_UI = '../ui/mks937b/info.ui'

DEVICE_MENU = 'mks937b/device_menu.py'
DEVICE_MENU_UI = '../ui/mks937b/device_menu.ui'

IOC_MAN = 'mks937b/ioc_man.py'
IOC_MAN_UI = '../ui/mks937b/ioc_man.ui'