#!/usr/bin/env python3
import os
import subprocess
import argparse as _argparse
import json

from siriushlacon.regatron.consts import COMPLETE_MAIN, REGATRON_DEVICES

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"

parser = _argparse.ArgumentParser(description="Run SI PS DCLink Interface.")
parser.add_argument("-dev", "--device", type=str, default="")
parser.add_argument("--master", action="store_true")
args = parser.parse_args()

isMaster = args.master
if not args.master:
    for data in REGATRON_DEVICES:
        if data["P"] == args.device:
            isMaster = data["master"] == 1

subprocess.Popen(
    "pydm --hide-nav-bar -m 'P={}, master={}' {}".format(
        args.device, "1" if isMaster else "0", COMPLETE_MAIN
    ),
    shell=True,
)
