#!/usr/bin/env python3
import argparse
import os

from siriushlacon.application import LogLevel, launch_pydm
from siriushlacon.mks937b.consts import MKS_MAIN

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"


if __name__ == "__main__":
    parser = argparse.ArgumentParser("VAC Pumps Controller")
    args = parser.parse_args()
    launch_pydm(displayfile=MKS_MAIN, hide_nav_bar=True, log_level=LogLevel.INFO)
