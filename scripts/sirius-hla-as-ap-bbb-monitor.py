#!/usr/bin/env python3
import subprocess
import os
import argparse
from siriushlacon.beaglebones.consts import BEAGLEBONES_MAIN

parser = argparse.ArgumentParser(description="Beaglebone monitor interface")
parser.add_argument(
    "--redis_host",
    type=str,
    default="",
    help="Redis server IP.",
    required=False,
    dest="redis_host",
)
args = parser.parse_args()

os.environ["PYDM_DEFAULT_PROTOCOL"] = "ca://"
pydm_args = ["--hide-nav-bar", "--hide-menu-bar", "--hide-status-bar"]
subprocess.Popen(
    "pydm {} --hide-nav-bar -m REDIS_HOST={} {}".format(
        " ".join(pydm_args), args.redis_host, BEAGLEBONES_MAIN
    ),
    shell=True,
)
