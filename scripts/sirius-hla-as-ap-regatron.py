#!/usr/bin/env python3
import subprocess
from siriushlacon.regatron.consts import REGATRON_MAIN

subprocess.Popen('pydm --hide-nav-bar '+ REGATRON_MAIN, shell=True)
