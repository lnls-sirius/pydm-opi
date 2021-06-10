Sirius HLA CONS - GUI
===========

This repo should contain every PyDM OPI developed by the CONS group currently in use.

[![Publish siriuspy to PyPI](https://github.com/lnls-sirius/pydm-opi/actions/workflows/pypi.yml/badge.svg)](https://github.com/lnls-sirius/pydm-opi/actions/workflows/pypi.yml)
[![Lint](https://github.com/lnls-sirius/pydm-opi/actions/workflows/lint.yml/badge.svg)](https://github.com/lnls-sirius/pydm-opi/actions/workflows/lint.yml)


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

#### Environment setup

Environment using a tested python version
```command
conda create --name py36 python=3.6
```

Environment dependencies:
```command
conda init powershell
conda activate py36
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install -c conda-forge/label/cf202003 epics-base
conda install qt==5.12.9 pyqt==5.12.3 pydm==1.10.4

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
