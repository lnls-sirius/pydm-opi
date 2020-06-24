#!/usr/bin/env python3
import subprocess
import os
from siriushlacon.agilent4uhv.consts import AGILENT_DEVICE_MAIN

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"

subprocess.Popen(
    "pydm -m DEVICE=asd,PREFIX_C1=c1,PREFIX_C2=c2,PREFIX_C3=c3,PREFIX_C4=c4 --hide-nav-bar "
    + AGILENT_DEVICE_MAIN,
    shell=True,
)
