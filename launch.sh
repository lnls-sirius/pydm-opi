#!/bin/bash
export PYTHONPATH=${PWD}

# PV Gateway Address
export EPICS_CA_AUTO_ADDR_LIST=YES

# PYDM expects the following language setup
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

OPTS=""
pydm $OPTS src/launcher.py
