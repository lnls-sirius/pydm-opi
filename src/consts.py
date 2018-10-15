#!/bin/bash
import os 
import platform

IS_LINUX = (os.name == 'posix' or platform.system() == 'Linux')
 
IOC_FILENAME = '/opt/stream-ioc/' + 'mks937_min.cmd'
ARCHIVER_URL = 'https://10.0.6.57/mgmt/ui/index.html' 

ARGS_HIDE_ALL = ['--hide-nav-bar', '--hide-menu-bar', '--hide-status-bar']
