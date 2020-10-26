#!/usr/bin/env python3
import os
import subprocess
import argparse as _argparse

from siriushlacon.regatron.consts import COMPLETE_MAIN, REGATRON_DEVICES

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"

parser = _argparse.ArgumentParser(description="Run SI PS DCLink Interface.")
parser.add_argument("-dev", "--device", type=str, default="")
parser.add_argument("--master", action="store_true")
args = parser.parse_args()

if args.device in REGATRON_DEVICES:
    isMaster = REGATRON_DEVICES[args.device]["master"]
    print("Master", isMaster, type(isMaster))
else:
    isMaster = args.master

subprocess.Popen(
    "pydm --hide-nav-bar -m 'P={}, master={}' {}".format(
        args.device, isMaster, COMPLETE_MAIN
    ),
    shell=True,
)
