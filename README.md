Sirius HLA CONS - GUI
===========

This repo should contain every PyDM OPI developed by the CONS group currently in use.

[![Build Status](https://api.travis-ci.org/lnls-sirius/pydm-opi.svg)](https://travis-ci.org/lnls-sirius/pydm-opi)
![Latest tag](https://img.shields.io/github/tag/lnls-sirius/pydm-opi.svg?style=flat)
[![Latest release](https://img.shields.io/github/release/lnls-sirius/pydm-opi.svg?style=flat)](https://github.com/lnls-sirius/pydm-opi/releases)
[![PyPI version fury.io](https://badge.fury.io/py/siriushlacon.svg)](https://pypi.python.org/pypi/siriushlacon/)
[![Read the Docs](https://readthedocs.org/projects/spack/badge/?version=latest)](https://lnls-sirius.github.io/pydm-opi/)
 
Install
-------
Available at **PyPi** https://pypi.org/project/siriushlacon/

```
pip install siriushlacon
```
Conda setup:
```
conda create -p /opt/conda/envs/cons python=3.8
conda install qt==5.12.9 pyqt==5.12.3 pydm==1.10.4
pip install siriushlacon
```

#### Manually

This repository depends on [PyDM](https://github.com/slaclab/pydm),
[PyEPICS](https://github.com/pyepics/pyepics), [conscommon](https://github.com/lnls-sirius/cons-common) and python>=3.6.
Dependencies listed at `requirements.txt`.

Clone from master or download the latest release.

### EPICS Base
Install EPICS and add it to PATH(Windows only)
```
https://epics.anl.gov/download/distributions/EPICSWindowsTools1.44-x64.msi
```
For linux users the recommended way is to compile the latest LTS release of [EPICS Base (R3.15.8)](https://github.com/epics-base/epics-base/tree/3.15).
The `<EPICS_BASE>/bin` folder must be added to the environment variable `PATH` and `<EPICS_BASE>/lib` folder to `LD_LIBRARY_PATH`.

### Sirius Environment
To install in a machine managed by [lnls-sirius/lnls-ansible](https://github.com/lnls-sirius/lnls-ansible) clone the repo recursively and make install as sudo.
```bash
cd ~/ && git clone --recursive https://github.com/lnls-sirius/pydm-opi && cd pydm-opi && sudo make install
```

### Desktop
In order to install the `.desktop` launcher:
```bash
make install-files
```
If using conda, remember to fix the Exec entry at the `.desktop' file accordingly:
```bash
/bin/bash -c 'source /opt/conda/etc/profile.d/conda.sh && conda activate cons && sirius-hla-as-ap-conlauncher.py'
```

Run
---
All scripts used to start the applications should be at the `bin` folder relative to the python installation environment, for example:
```bash
~/.local/bin
/usr/local/bin
...
```

To launch the main window use the script: `sirius-hla-as-ap-conlauncher.py`

### Windows
There should be no problems running on windows.
