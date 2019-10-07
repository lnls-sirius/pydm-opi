#!/usr/bin/env python3
import subprocess
from siriushlacon.pctrl.consts import PCTRL_MAIN 

subprocess.Popen('pydm --hide-nav-bar '+ PCTRL_MAIN, shell=True)
