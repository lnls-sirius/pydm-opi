#!/usr/bin/env python3
import subprocess
from siriushlacon.agilent4uhv.consts import AGILENT_OVERVIEW


macros = '\'{"device": "UHV", "TYPE": "SR", "FORMAT": "EXP", '\
         ' "TITLE": "ION Pump Agilent 4UHV - SR and TS"}\''

subprocess.Popen('pydm --hide-nav-bar -m '+macros +
                 ' '+AGILENT_OVERVIEW, shell=True)
