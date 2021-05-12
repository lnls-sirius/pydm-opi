Sirius HLA CONS - GUI
===========

This repo should contain every PyDM OPI developed by the CONS group currently in use.

[![PyPi Deploy](https://api.travis-ci.org/lnls-sirius/pydm-opi.svg)](https://travis-ci.org/lnls-sirius/pydm-opi)
[![Lint](https://github.com/lnls-sirius/pydm-opi/actions/workflows/lint.yml/badge.svg)](https://github.com/lnls-sirius/pydm-opi/actions/workflows/lint.yml)
![Latest tag](https://img.shields.io/github/tag/lnls-sirius/pydm-opi.svg?style=flat)
[![Latest release](https://img.shields.io/github/release/lnls-sirius/pydm-opi.svg?style=flat)](https://github.com/lnls-sirius/pydm-opi/releases)
[![PyPI version fury.io](https://badge.fury.io/py/siriushlacon.svg)](https://pypi.python.org/pypi/siriushlacon/)
[![Read the Docs](https://readthedocs.org/projects/spack/badge/?version=latest)](https://lnls-sirius.github.io/pydm-opi/)

Develop
-------
In order to contribute with this repository the developer must have **pre-commit** installed locally.
```command
pip install pre-commit
pre-commit install
```

Install
-------
[Windows instructions](miscellaneous/windows).

Available at **PyPi** https://pypi.org/project/siriushlacon/, can be installed using pip but specific versions of QT are needed.

```command
pip install siriushlacon
```

Conda setup:
```command
# Install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh

# Remove the install script
rm Miniconda3-latest-Linux-x86_64.sh

# Optionally create an environment using a tested python version
conda create -p /opt/conda/envs/cons python=3.8

# Dependencies
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install qt==5.12.9 pyqt==5.12.3 pydm==1.10.4

pip install siriushlacon
```

### EPICS Base
Install EPICS and add it to PATH(Windows only)
```
https://epics.anl.gov/download/distributions/EPICSWindowsTools1.44-x64.msi
```
For linux users the recommended way is to compile the latest LTS release of [EPICS Base (R3.15.8)](https://github.com/epics-base/epics-base/tree/3.15).
The `<EPICS_BASE>/bin` folder must be added to the environment variable `PATH` and `<EPICS_BASE>/lib` folder to `LD_LIBRARY_PATH`.

### Desktop
In order to install the `.desktop` launcher:
```command
make install-files
```
If using conda, remember to fix the Exec entry at the `.desktop' file accordingly:
```bash
/bin/bash -c 'source /opt/conda/etc/profile.d/conda.sh && conda activate cons && sirius-hla-as-ap-conlauncher.py'
```

Run
---
To launch the main window use the script: `sirius-hla-as-ap-conlauncher.py`. On Windows make sure that the correct `python.exe` is the default program for `*.py` files.

