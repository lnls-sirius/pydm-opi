import subprocess
from siriushlacon.agilent4uhv.consts import AGILENT_OVERVIEW


macros = '\'{"device": "UHV", "TYPE": "BO", "FORMAT": "EXP", '\
         ' "TITLE": "ION Pump Agilent 4UHV - BO and TB"}\''

subprocess.Popen('pydm --hide-nav-bar -m '+macros +
                 ' '+AGILENT_OVERVIEW, shell=True)
