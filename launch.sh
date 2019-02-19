#!/bin/bash
function cleanup {
    deactivate
    echo "  Bye !  "
}

#source .virtualenv/bin/activate
trap cleanup EXIT

export PYTHONPATH=${PWD}
export HOME=${PWD}

# PV Gateway Address
export EPICS_CA_ADDR_LIST=10.0.6.57
export EPICS_CA_AUTO_ADDR_LIST=YES

# PYDM expects the following language setup
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

OPTS=""
pydm $OPTS src/launcher.py
