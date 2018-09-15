#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform

IS_LINUX =  (os.name == 'posix' or platform.system() == 'Linux')

COLD_CATHODE = 'CC'
PIRANI = 'PR'
NONE  = 'None' 

IOC_FILENAME = '/opt/stream-ioc/' + 'mks937_min.cmd'
ARCHIVER_URL = 'https://10.0.6.57/mgmt/ui/index.html' 

DEVICE_PREFIX = "VGC"
ARGS_HIDE_ALL =  ['--hide-nav-bar', '--hide-menu-bar', '--hide-status-bar']


MAIN_UI = '../ui/main.ui'

STORAGE_RING_PY = 'storage_ring.py'
STORAGE_RING_UI = '../ui/storage_ring.ui'

BOOSTER_PY = 'booster.py'
BOOSTER_UI = '../ui/booster.ui'

BTS_PY = 'bts.py'
BTS_UI = '../ui/bts.ui'

LTB_PY = 'ltb.py'
LTB_UI = '../ui/ltb.ui'

NONE_UI = '../ui/none.ui'

DEVICE_PREVIEW_PY = 'device_preview.py'
DEVICE_PREVIEW_UI = '../ui/device_preview.ui'

CC_UI = '../ui/cc.ui' 
CC_PY = 'cc.py' 

PR_UI = '../ui/pirani.ui'
PR_PY = 'pirani.py'

PRESSURE_PY = 'pressure.py'
if IS_LINUX:
    PRESSURE_UI = '../ui/pressure.ui'
else:
    PRESSURE_UI = '../ui/pressure_win.ui'

SETTINGS_PY = 'settings.py'
SETTINGS_UI = '../ui/settings.ui'

INFO_PY = 'info.py'
INFO_UI = '../ui/info.ui'

DEVICE_MENU_PY = 'device_menu.py'
DEVICE_MENU_UI = '../ui/device_menu.ui'

IOC_MAN_PY = 'ioc_man.py'
IOC_MAN_UI = '../ui/ioc_man.ui'

ring_sub_sectors = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
ring_sector_devices = [
    ['1', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['2', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['3', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['4', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['5', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['6', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['7', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['8', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['9', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['10', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['11', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['12', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['13', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['14', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['15', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['16', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['16', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['17', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['18', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['20', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['21', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['22', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['23', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['24', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['25', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['26', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['27', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['28', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['29', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['30', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['31', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['32', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['33', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['34', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['35', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['36', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['37', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['38', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['39', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['40', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['41', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['42', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['43', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['44', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['45', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['46', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['47', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['48', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['49', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['50', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['51', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['52', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['53', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['54', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['55', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['56', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['57', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['58', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['59', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['60', COLD_CATHODE, COLD_CATHODE, PIRANI]
]

booster_sub_sectors = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
booster_sector_devices = [
    ['1', PIRANI, PIRANI, PIRANI],
    ['2', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['3', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['4', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['5', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['6', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['7', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['8', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['9', COLD_CATHODE, COLD_CATHODE, PIRANI],
    ['10', COLD_CATHODE, COLD_CATHODE, PIRANI]
]

ltb_sub_sectors = ['1']
ltb_sector_devices = [
    ['1', COLD_CATHODE, COLD_CATHODE, PIRANI]
]

bts_sub_sectors = ['1']
bts_sector_devices = [
    ['Another:BTS-Device', PIRANI, PIRANI, PIRANI],
    ['Just-a-Random:Dev', COLD_CATHODE, COLD_CATHODE, COLD_CATHODE]
]