#!/bin/bash
export PYTHONPATH=${PWD}
export HOME=${PWD}

# PV Gateway Address
export EPICS_CA_ADDR_LIST="127.0.0.1:5470"

# PYDM expects the following language setup
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

#OPTS="--hide-nav-bar --hide-menu-bar --hide-status-bar"
OPTS=""
pydm $OPTS src/launcher.py
