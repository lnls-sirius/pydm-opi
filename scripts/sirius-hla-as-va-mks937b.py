#!/usr/bin/env python3
import os
import subprocess

from siriushlacon.mks937b.consts import MKS_MAIN

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"

subprocess.Popen("pydm --hide-nav-bar " + MKS_MAIN, shell=True)
