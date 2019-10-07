#!/usr/bin/env python3
import subprocess
from siriushlacon.launcher.consts import LAUNCH_WINDOW
from siriushlacon.tools.consts import PYDM_TOOLS_PATH


subprocess.Popen('PYDM_TOOLS_PATH={} pydm --hide-nav-bar {}'
    .format(PYDM_TOOLS_PATH, LAUNCH_WINDOW), shell=True)
