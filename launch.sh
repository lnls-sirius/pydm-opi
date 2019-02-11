#!/bin/bash
function cleanup {
    deactivate
    echo "  Bye !  "
}

source .virtualenv/bin/activate
trap cleanup EXIT

git pull

export PYTHONPATH=${PWD}
export HOME=${PWD}

# PV Gateway Address
export EPICS_CA_ADDR_LIST=10.0.38.34

# PYDM expects the following language setup
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

#OPTS="--hide-nav-bar --hide-menu-bar --hide-status-bar"
OPTS=""
pydm $OPTS src/launcher.py
