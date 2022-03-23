Sirius HLA CONS - GUI
===========

This repo contains various PyDM OPIs in use.

[![Publish siriuspy to PyPI](https://github.com/lnls-sirius/pydm-opi/actions/workflows/pypi.yml/badge.svg)](https://github.com/lnls-sirius/pydm-opi/actions/workflows/pypi.yml)
[![Lint](https://github.com/lnls-sirius/pydm-opi/actions/workflows/lint.yml/badge.svg)](https://github.com/lnls-sirius/pydm-opi/actions/workflows/lint.yml)
[![Test and Coverage](https://github.com/lnls-sirius/pydm-opi/actions/workflows/tests.yml/badge.svg)](https://github.com/lnls-sirius/pydm-opi/actions/workflows/tests.yml)


![Latest tag](https://img.shields.io/github/tag/lnls-sirius/pydm-opi.svg?style=flat)
[![Latest release](https://img.shields.io/github/release/lnls-sirius/pydm-opi.svg?style=flat)](https://github.com/lnls-sirius/pydm-opi/releases)
[![PyPI version fury.io](https://badge.fury.io/py/siriushlacon.svg)](https://pypi.python.org/pypi/siriushlacon/)

[![Read the Docs](https://readthedocs.org/projects/spack/badge/?version=latest)](https://lnls-sirius.github.io/pydm-opi/)

Develop
-------
In order to contribute with this repository the developer must have **pre-commit** installed and enabled.
```command
pip install pre-commit
pre-commit install
```

Install
-------
[Windows instructions](miscellaneous/windows).

Available at **PyPi** https://pypi.org/project/siriushlacon/, can be installed using pip but specific versions of QT are needed.

### Conda

#### Install (Linux)
```command
# Install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh

# Remove the install script
rm Miniconda3-latest-Linux-x86_64.sh
```

#### Install (Windows)

Download at https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe

**Important**

- Local installation (single user only).
- Add to the PATH

The user should check if conda is enabled. The powershell prompt should look like:
```powershell
(base) ...
```

In order to setup conda correctly on powershell use the command below then restart the shell application:
```powershell
conda init powershell
```

Set the powershell execution policy so external scripts are availble https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-7.1

```powershell
Set-ExecutionPolicy RemoteSigned
```

#### Environment setup

Create a conda environment using a tested python version
```command
conda create --name py36 python=3.6
```

Environment dependencies:
```command
# Activate the environment "py36", the shell prompt should start with "(py36) ..."
conda activate py36

# Enable conda-forge channel
conda config --add channels conda-forge
conda config --set channel_priority strict

# Install EPICS base
conda install -c conda-forge/label/cf202003 epics-base

# Install dependencies
conda install -c conda-forge bottleneck
conda install -c conda-forge pyqt==5.12.3
conda install -c conda-forge qt==5.12.9
conda install -c conda-forge pydm==1.10.4

# Install interfaces
pip install --upgrade siriushlacon
```

## Desktop shortcut
### Windows:
This assumes a conda environment named `py36`. The `.lnk` content must be updated in case of a different name.
```powershell
iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/lnls-sirius/pydm-opi/master/miscellaneous/windows/Create-Shortcut.ps1'));
```

Run
---
To launch the main window use the script: `sirius-hla-as-ap-conlauncher.py`.

On Windows make sure that the correct `python.exe` or `pythonw.exe` is the default program for `*.py` files.

```powershell
pythonw.exe (Get-Command sirius-hla-as-ap-conlauncher.py).Path
pythonw.exe (Get-Command sirius-hla-as-va-vbc.py).Path
```
