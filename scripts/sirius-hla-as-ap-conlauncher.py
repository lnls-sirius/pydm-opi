#!/usr/bin/env python3
import os

from siriushlacon.application import LogLevel, launch_pydm
from siriushlacon.launcher.consts import LAUNCH_WINDOW
from siriushlacon.tools.consts import PYDM_TOOLS_PATH
from siriushlacon.vbc.consts import BBB_IOC_ADDR

if __name__ == "__main__":
    os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "YES"
    os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"
    os.environ["PYDM_TOOLS_PATH"] = PYDM_TOOLS_PATH

    if "EPICS_CA_ADDR_LIST" not in os.environ:
        os.environ["EPICS_CA_ADDR_LIST"] = " ".join(BBB_IOC_ADDR)
    else:
        os.environ["EPICS_CA_ADDR_LIST"] = (
            " ".join(BBB_IOC_ADDR) + os.environ["EPICS_CA_ADDR_LIST"]
        )

    launch_pydm(
        displayfile=LAUNCH_WINDOW,
        hide_nav_bar=True,
        log_level=LogLevel.INFO,
    )
