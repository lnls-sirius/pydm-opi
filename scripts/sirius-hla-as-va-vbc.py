#!/usr/bin/env python3
import subprocess
import os
from siriushlacon.vbc.consts import MAIN_WINDOW_PY as VBC_MAIN_WINDOW_PY

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"

subprocess.Popen(
    f"pydm --hide-nav-bar {VBC_MAIN_WINDOW_PY}", shell=True
)
