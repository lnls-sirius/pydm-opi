#!/usr/bin/env python3
import os
import subprocess

from siriushlacon.mks937b.consts import MKS_OVERVIEW

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"

macros = '\'{"device": "MKS", "TYPE": "IT", "TITLE": "MKS 937b - IT"}\''
subprocess.Popen("pydm --hide-nav-bar -m " + macros + " " + MKS_OVERVIEW, shell=True)
