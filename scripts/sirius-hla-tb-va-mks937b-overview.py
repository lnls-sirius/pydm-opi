#!/usr/bin/env python3
import subprocess
import os
from siriushlacon.mks937b.consts import MKS_OVERVIEW


os.environ['PYDM_DEFAULT_PROTOCOL'] = 'ca://'
macros = '\'{"device": "MKS", "TYPE": "TB", "TITLE": "MKS 937b - TB"}\''

subprocess.Popen('pydm --hide-nav-bar -m '+macros+' '+MKS_OVERVIEW, shell=True)
