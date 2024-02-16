Sirius HLA CONS - GUI
=====================

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

Available at **PyPi** https://pypi.org/project/siriushlacon/.

#### Mamba/Micromamba Environment setup

We recommend the use of [Mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html#fresh-install-recommended)/[Micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html#manual-installation) environments for deploying in linux or windows.

An environment can be installed by creating a file named siriushlacon-env.yml with the following contents:

```command
name: siriushlacon
channels:
  - conda-forge
dependencies:
  - python=3.8
  - epics-base
  - numpy<1.20
  - matplotlib==3.3.4
  - pyqt==5.12.3
  - pydm==1.10.4
  - pip:
    - siriushlacon
```

and running, for linux:
```command
mamba/micromamba create -f siriushlacon-env.yml
```

or, for windows:
```command
mamba/micromamba create -f siriushlacon-env.yml
```
