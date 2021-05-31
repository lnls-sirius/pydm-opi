#!/usr/bin/env python3
import os
import subprocess

from siriushlacon.launcher.consts import LAUNCH_WINDOW
from siriushlacon.tools.consts import PYDM_TOOLS_PATH

os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "YES"
os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"
os.environ["PYDM_TOOLS_PATH"] = PYDM_TOOLS_PATH

BBB_IOC_ADDR = [
    "10.128.40.1:5064",
    "10.128.40.1:5068",
    "10.128.40.2:5064",
    "10.128.40.2:5068",
    "10.128.40.3:5064",
    "10.128.40.3:5068",
    "10.128.40.4:5064",
    "10.128.40.4:5068",
    "10.128.40.5:5064",
    "10.128.40.5:5068",
    "10.128.40.6:5064",
    "10.128.40.6:5068",
    "10.128.40.7:5064",
    "10.128.40.7:5068",
    "10.128.40.8:5064",
    "10.128.40.8:5068",
    "10.128.40.9:5064",
    "10.128.40.9:5068",
    "10.128.40.10:5064",
    "10.128.40.10:5068",
]

if "EPICS_CA_ADDR_LIST" not in os.environ:
    os.environ["EPICS_CA_ADDR_LIST"] = " ".join(BBB_IOC_ADDR)
else:
    os.environ["EPICS_CA_ADDR_LIST"] = (
        " ".join(BBB_IOC_ADDR) + os.environ["EPICS_CA_ADDR_LIST"]
    )

subprocess.Popen("pydm --hide-nav-bar {}".format(LAUNCH_WINDOW), shell=True)
