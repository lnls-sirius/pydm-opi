#!/usr/bin/env python3
import os
import subprocess
import argparse as _argparse
from siriushlacon.mks937b.consts import MKS_GRAPH, MKS_OVERVIEW

parser = _argparse.ArgumentParser(description="Run BO MKS Overview.")
parser.add_argument("-graph", action="store_true")
args = parser.parse_args()

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"

if args.graph:
    f = MKS_GRAPH
    macros = '\'{"TYPE": "BO"}\''
else:
    f = MKS_OVERVIEW
    macros = '\'{"device": "MKS", "TYPE": "BO", "TITLE": "MKS 937b - BO"}\''


subprocess.Popen("pydm --hide-nav-bar -m " + macros + " " + f, shell=True)
