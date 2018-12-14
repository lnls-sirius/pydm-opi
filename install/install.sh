#!/bin/bash
apt-get -y install python3-pip python3-dev
pip3 install virtualenv==16.0.0 && \
virtualenv ../.virtualenv

pushd ../.virtualenv/bin
    source activate
    echo "Using Python 3 "${PWD}
popd

echo "Installing requirements ..."
pip3 install -r requirements.txt
deactivate
