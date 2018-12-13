#!/bin/bash
pushd ../.virtualenv/bin
    source activate
    echo "Using Python 3 "${PWD}
popd

echo "Installing requirements ..."
pip3 install -r requirements.txt
deactivate
