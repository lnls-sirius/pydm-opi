#!/usr/bin/env python3
import subprocess
from siriushlacon.mks937b.consts import MKS_MAIN


subprocess.Popen('pydm --hide-nav-bar '+MKS_MAIN, shell=True)
