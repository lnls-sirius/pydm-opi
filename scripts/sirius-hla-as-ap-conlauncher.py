#!/usr/bin/env python3
import subprocess
import os
from siriushlacon.launcher.consts import LAUNCH_WINDOW
from siriushlacon.tools.consts import PYDM_TOOLS_PATH

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"
os.environ["PYDM_TOOLS_PATH"] = PYDM_TOOLS_PATH

subprocess.Popen("pydm --hide-nav-bar {}".format(LAUNCH_WINDOW), shell=True)
