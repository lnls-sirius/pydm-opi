#!/usr/bin/env python3
import subprocess
import os
from siriushlacon.beaglebones.consts import BEAGLEBONES_MAIN


os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"
subprocess.Popen("pydm --hide-nav-bar " + BEAGLEBONES_MAIN, shell=True)
