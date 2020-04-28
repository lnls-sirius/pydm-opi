#!/usr/bin/env python3
import subprocess
import os
from siriushlacon.regatron.consts import REGATRON_MAIN

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"
subprocess.Popen("pydm --hide-nav-bar " + REGATRON_MAIN, shell=True)
