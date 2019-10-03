import subprocess
from siriushlacon.launcher.consts import LAUNCH_WINDOW


subprocess.Popen('pydm --hide-nav-bar '+LAUNCH_WINDOW, shell=True)
