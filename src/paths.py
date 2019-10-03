#!/usr/bin/python3
import os
import platform

IS_LINUX = (os.name == 'posix' or platform.system() == 'Linux')


def get_abs_path(relative):
    """
    relative = relative path with base at python/
    """
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), relative)


DRAW_ALARMS_NO_INVALID_QSS = ''
with open(get_abs_path('../css/draw_no-invalid.qss')) as f:
    DRAW_ALARMS_NO_INVALID_QSS = ''.join(f.readlines())

TABLE_ALARMS_QSS = ''
with open(get_abs_path('../css/table-alarm.qss')) as f:
    TABLE_ALARMS_QSS = ''.join(f.readlines())


LAUNCH_WINDOW = "launcher/launcher.py"
LAUNCH_WINDOW_UI = "../ui/launcher.ui"

OVERVIEW_UI = '../ui/overview.ui'

PCTRL_MAIN = '../ui/pctrl/main.py'

EPP_MAIN = '../ui/spixconv/launch_ui_main_window.py'

###############################################################################
#                                   MBTemp                                    #
###############################################################################
MBTEMP_MAIN = 'mbtemp/main.py'
MBTEMP_MAIN_UI = '../ui/mbtemp/main.ui'

###############################################################################
#                                  Agilent                                    #
###############################################################################
AGILENT_OVERVIEW = 'agilent4uhv/overview.py'

AGILENT_MAIN = "agilent4uhv/main.py"
AGILENT_MAIN_UI = "../ui/agilent4uhv/main.ui"

AGILENT_DEVICE_MAIN = "agilent4uhv/device_main.py"
AGILENT_DEVICE_MAIN_UI = "../ui/agilent4uhv/device_main.ui"

# AGILENT_DEVICE = "agilent4uhv/device.py"
AGILENT_DEVICE_UI = "../ui/agilent4uhv/device.ui"

# AGILENT_CHANNEL = "agilent4uhv/channel.py"
AGILENT_CHANNEL_UI = "../ui/agilent4uhv/channel.ui"

###############################################################################
#                                      MKS                                    #
###############################################################################
MKS_OVERVIEW = 'mks937b/overview.py'

MKS_MAIN = "mks937b/table.py"
MKS_MAIN_UI = "../ui/mks937b/table.ui"

TABLE = 'mks937b/table.py'
TABLE_UI = '../ui/mks937b/table.ui'

# STORAGE_RING = 'mks937b/storage_ring.py'
STORAGE_RING_UI = '../ui/mks937b/storage_ring.ui'

# BOOSTER = 'mks937b/booster.py'
BOOSTER_UI = '../ui/mks937b/booster.ui'

# BTS = 'mks937b/bts.py'
BTS_UI = '../ui/mks937b/bts.ui'

# LTB = 'mks937b/ltb.py'
LTB_UI = '../ui/mks937b/ltb.ui'

NONE_UI = '../ui/mks937b/none.ui'

DEVICE_PREVIEW = 'mks937b/device_preview.py'
DEVICE_PREVIEW_UI = '../ui/mks937b/device_preview.ui'

# CC = 'mks937b/cc.py'
CC_UI = '../ui/mks937b/cc.ui'

# PR = 'mks937b/pirani.py'
PR_UI = '../ui/mks937b/pirani.ui'

PRESSURE = 'mks937b/pressure.py'
PRESSURE_UI = '../ui/mks937b/pressure.ui'

SETTINGS = 'mks937b/settings.py'
SETTINGS_UI = '../ui/mks937b/settings.ui'

# INFO = 'mks937b/info.py'
INFO_UI = '../ui/mks937b/info.ui'

DEVICE_MENU = 'mks937b/device_menu.py'
DEVICE_MENU_UI = '../ui/mks937b/device_menu.ui'

# IOC_MAN = 'mks937b/ioc_man.py'
IOC_MAN_UI = '../ui/mks937b/ioc_man.ui'
