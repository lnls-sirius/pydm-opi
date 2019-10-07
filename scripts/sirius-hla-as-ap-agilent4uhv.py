#!/usr/bin/env python3
import subprocess
from siriushlacon.agilent4uhv.consts import AGILENT_MAIN


subprocess.Popen('pydm --hide-nav-bar '+AGILENT_MAIN, shell=True)
