#!/usr/bin/env python3
import subprocess
import os
from siriushlacon.countingpru.consts import GAMMA_COUNTING_MAIN


os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"
subprocess.Popen("pydm --hide-nav-bar " + GAMMA_COUNTING_MAIN, shell=True)
