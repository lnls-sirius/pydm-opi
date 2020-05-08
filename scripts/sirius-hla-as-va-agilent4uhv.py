#!/usr/bin/env python3
import subprocess
import os
from siriushlacon.agilent4uhv.consts import AGILENT_MAIN

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"

subprocess.Popen("pydm --hide-nav-bar " + AGILENT_MAIN, shell=True)
