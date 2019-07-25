#!/bin/bash
export PYTHONPATH=${PWD}
ping -c 1 10.0.38.42
if [ $?=0 ]; then
    rm Redes\ e\ Beaglebones.xlsx*
    wget http://10.0.38.42/streamdevice-ioc/Redes%20e%20Beaglebones.xlsx
fi
OPT="--hide-nav-bar --hide-menu-bar --hide-status-bar"
pydm $OPT src/launcher.py
