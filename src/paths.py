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
LAUNCH_WINDOW_UI = "launcher/ui/launcher.ui"

OVERVIEW_UI = 'utils/ui/overview.ui'

PCTRL_MAIN = 'pctrl/main.py'

EPP_MAIN = '../ui/spixconv/launch_ui_main_window.py'

###############################################################################
#                                   MBTemp                                    #
###############################################################################
MBTEMP_MAIN = 'mbtemp/main.py'
MBTEMP_MAIN_UI = 'mbtemp/ui/main.ui'

###############################################################################
#                                  Agilent                                    #
###############################################################################
AGILENT_OVERVIEW = 'agilent4uhv/overview.py'

AGILENT_MAIN = "agilent4uhv/main.py"
AGILENT_MAIN_UI = "agilent4uhv/ui/main.ui"

AGILENT_DEVICE_MAIN = "agilent4uhv/device_main.py"
AGILENT_DEVICE_MAIN_UI = "agilent4uhv/ui/device_main.ui"

# AGILENT_DEVICE = "agilent4uhv/device.py"
AGILENT_DEVICE_UI = "agilent4uhv/ui/device.ui"

# AGILENT_CHANNEL = "agilent4uhv/channel.py"
AGILENT_CHANNEL_UI = "agilent4uhv/ui/channel.ui"

###############################################################################
#                                      MKS                                    #
###############################################################################
MKS_OVERVIEW = 'mks937b/overview.py'

MKS_MAIN = "mks937b/table.py"
MKS_MAIN_UI = "mks937b/ui/table.ui"

TABLE = 'mks937b/table.py'
TABLE_UI = 'mks937b/ui/table.ui'

# STORAGE_RING = 'mks937b/storage_ring.py'
STORAGE_RING_UI = 'mks937b/ui/storage_ring.ui'

# BOOSTER = 'mks937b/booster.py'
BOOSTER_UI = 'mks937b/ui/booster.ui'

# BTS = 'mks937b/bts.py'
BTS_UI = 'mks937b/ui/bts.ui'

# LTB = 'mks937b/ltb.py'
LTB_UI = 'mks937b/ui/ltb.ui'

NONE_UI = 'mks937b/ui/none.ui'

DEVICE_PREVIEW = 'mks937b/device_preview.py'
DEVICE_PREVIEW_UI = 'mks937b/ui/device_preview.ui'

# CC = 'mks937b/cc.py'
CC_UI = 'mks937b/ui/cc.ui'

# PR = 'mks937b/pirani.py'
PR_UI = 'mks937b/ui/pirani.ui'

PRESSURE = 'mks937b/pressure.py'
PRESSURE_UI = 'mks937b/ui/pressure.ui'

SETTINGS = 'mks937b/settings.py'
SETTINGS_UI = 'mks937b/ui/settings.ui'

# INFO = 'mks937b/info.py'
INFO_UI = 'mks937b/ui/info.ui'

DEVICE_MENU = 'mks937b/device_menu.py'
DEVICE_MENU_UI = 'mks937b/ui/device_menu.ui'

# IOC_MAN = 'mks937b/ioc_man.py'
IOC_MAN_UI = 'mks937b/ui/ioc_man.ui'
