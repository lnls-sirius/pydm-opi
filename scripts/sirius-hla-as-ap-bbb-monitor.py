#!/usr/bin/env python3
import subprocess
import os
from siriushlacon.beaglebones.consts import BEAGLEBONES_MAIN


os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"
subprocess.Popen("python " + BEAGLEBONES_MAIN, shell=True)
