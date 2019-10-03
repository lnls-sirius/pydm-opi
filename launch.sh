#!/bin/bash
export PYTHONPATH=${PWD}
OPT="--hide-nav-bar --hide-menu-bar --hide-status-bar"
pydm $OPT src/launcher/launcher.py
