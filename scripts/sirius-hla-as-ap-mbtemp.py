#!/usr/bin/env python3
import subprocess
import os
from siriushlacon.mbtemp.consts import MBTEMP_MAIN


os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"
subprocess.Popen("pydm --hide-nav-bar " + MBTEMP_MAIN, shell=True)
