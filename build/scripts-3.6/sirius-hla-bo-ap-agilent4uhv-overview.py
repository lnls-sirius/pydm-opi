#!/usr/bin/python3
import subprocess
import os
from siriushlacon.agilent4uhv.consts import AGILENT_OVERVIEW


os.environ['PYDM_DEFAULT_PROTOCOL'] = 'ca://'
macros = '\'{"device": "UHV", "TYPE": "BO", "FORMAT": "EXP", '\
         ' "TITLE": "ION Pump Agilent 4UHV - BO and TB"}\''

subprocess.Popen('pydm --hide-nav-bar -m '+macros +
                 ' '+AGILENT_OVERVIEW, shell=True)
