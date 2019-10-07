#!/usr/local/env python3
import subprocess
from siriushlacon.mks937b.consts import MKS_OVERVIEW


macros = '\'{"device": "MKS", "TYPE": "SR", "TITLE": "MKS 937b - SI and TS"}\''

subprocess.Popen('pydm --hide-nav-bar -m '+macros+' '+MKS_OVERVIEW, shell=True)
