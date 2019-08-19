#!/bin/bash
import os
import platform
import logging
logger = logging.getLogger()

res = os.system('wget -T 1 -r --tries=2 http://10.0.38.42/streamdevice-ioc/Redes%20e%20Beaglebones.xlsx -O /var/tmp/pydm-opi')
if int(res) != 0:
    logger.warning('Failed to update the spreadsheet from http://10.0.38.42/streamdevice-ioc/Redes%20e%20Beaglebones.xlsx ! Using old data ...')
    FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../../Redes e Beaglebones.xlsx')
else:
    FILE = '/var/tmp/pydm-opi'
IS_LINUX = (os.name == 'posix' or platform.system() == 'Linux')

IOC_FILENAME = '/opt/stream-ioc/' + 'mks937_min.cmd'
ARCHIVER_URL = 'https://10.0.6.57/mgmt/ui/index.html'

ARGS_HIDE_ALL = ['--hide-nav-bar', '--hide-menu-bar', '--hide-status-bar']

ARCHIVER_URL = 'https://10.0.6.57/mgmt/ui/index.html'
