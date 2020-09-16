#!/usr/bin/env python3
import os
import subprocess
import argparse as _argparse
import json
from siriushlacon.regatron.consts import COMPLETE_MAIN

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"

parser = _argparse.ArgumentParser(description="Run SI PS DCLink Interface.")
parser.add_argument("-dev", "--device", type=str, default="")
args = parser.parse_args()
subprocess.Popen(
    "pydm --hide-nav-bar -m P={} {}".format(args.device, COMPLETE_MAIN), shell=True
)
