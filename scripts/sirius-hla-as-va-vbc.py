#!/usr/bin/env python3
import subprocess
import os
from siriushlacon.vbc.consts import MAIN_WINDOW_PY as VBC_MAIN_WINDOW_PY

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"

os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "YES"

if "EPICS_CA_ADDR_LIST" not in os.environ:
    os.environ["EPICS_CA_ADDR_LIST"] = "10.128.40.2:5068"
else:
    os.environ["EPICS_CA_ADDR_LIST"] = "10.128.40.2:5068" + os.environ["EPICS_CA_ADDR_LIST"]


subprocess.Popen(
    f"pydm --hide-nav-bar {VBC_MAIN_WINDOW_PY}", shell=True
)
