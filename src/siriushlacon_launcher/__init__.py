#!/usr/bin/env python
import argparse
import inspect
import json
import os

from siriushlacon.application import LogLevel, launch_pydm
from siriushlacon.launcher.consts import LAUNCH_WINDOW
from siriushlacon.logging import get_logger
from siriushlacon.tools.consts import PYDM_TOOLS_PATH
from siriushlacon.vbc.consts import BBB_IOC_ADDR
from siriushlacon.vbc.consts import MAIN_WINDOW_PY as VBC_MAIN_WINDOW_PY

logger = get_logger("")


def _config_environment():
    os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "YES"
    os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"
    os.environ["PYDM_TOOLS_PATH"] = PYDM_TOOLS_PATH

    if "EPICS_CA_ADDR_LIST" not in os.environ:
        os.environ["EPICS_CA_ADDR_LIST"] = " ".join(BBB_IOC_ADDR)
    else:
        os.environ["EPICS_CA_ADDR_LIST"] = (
            " ".join(BBB_IOC_ADDR) + os.environ["EPICS_CA_ADDR_LIST"]
        )


def launch_generic():
    _config_environment()
    parser = argparse.ArgumentParser("Generic Launcher")
    parser.add_argument(
        "params",
        help=f"json str to be forwarded into `launch_pydm(`{inspect.signature(launch_pydm).__str__()})",
    )
    args = parser.parse_args()
    data = json.loads(args.params)
    logger.info(f"Launch siriushlacon PyDM OPI - {data}")
    launch_pydm(**data)


def launch_main_window():
    _config_environment()
    launch_pydm(
        displayfile=LAUNCH_WINDOW,
        hide_nav_bar=True,
        log_level=LogLevel.INFO,
    )


def launch_vbc():
    parser = argparse.ArgumentParser("VAC Pumps Controller")
    parser.parse_args()
    launch_pydm(
        displayfile=VBC_MAIN_WINDOW_PY, hide_nav_bar=True, log_level=LogLevel.INFO
    )
