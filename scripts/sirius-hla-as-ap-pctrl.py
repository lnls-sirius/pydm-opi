#!/usr/bin/env python3
import subprocess
import os
from siriushlacon.pctrl.consts import PCTRL_MAIN

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"
subprocess.Popen("pydm --hide-nav-bar " + PCTRL_MAIN, shell=True)
