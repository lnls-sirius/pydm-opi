import subprocess
from siriushlacon.mks937b.consts import MKS_OVERVIEW


macros = '\'{"device": "MKS", "TYPE": "BO", "TITLE": "MKS 937b - BO and TB"}\''

subprocess.Popen('pydm --hide-nav-bar -m '+macros+' '+MKS_OVERVIEW, shell=True)
