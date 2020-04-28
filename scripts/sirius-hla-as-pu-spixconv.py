#!/usr/bin/env python3
import subprocess
from siriushlacon.spixconv.consts import SPIXCONV_MAIN


subprocess.Popen("pydm --hide-nav-bar " + SPIXCONV_MAIN, shell=True)
