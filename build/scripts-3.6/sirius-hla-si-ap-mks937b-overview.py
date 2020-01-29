#!/usr/bin/python3
import subprocess
import os
from siriushlacon.mks937b.consts import MKS_OVERVIEW


os.environ['PYDM_DEFAULT_PROTOCOL'] = 'ca://'
macros = '\'{"device": "MKS", "TYPE": "SR", "TITLE": "MKS 937b - SI and TS"}\''

subprocess.Popen('pydm --hide-nav-bar -m '+macros+' '+MKS_OVERVIEW, shell=True)
