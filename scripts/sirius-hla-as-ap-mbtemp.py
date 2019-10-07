#!/usr/bin/env python3
import subprocess
from siriushlacon.mbtemp.consts import MBTEMP_MAIN


subprocess.Popen('pydm --hide-nav-bar '+MBTEMP_MAIN, shell=True)
