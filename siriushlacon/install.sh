#!/bin/bash
set -e
set -x
NAME=pydm-opi

DESKTOP=/home/$(whoami)/Desktop
if [ -d $DESKTOP ]; then
    echo 'ok'
else
    echo 'Desktop folder not found!'
    exit 1
fi
cat ${NAME}.desktop.template | D=$(pwd) envsubst > $DESKTOP/${NAME}.desktop
