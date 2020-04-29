CONS OPIs
===========

This repo should contain every PyDM OPI developed by the CONS group currently in use.

[Read the docs !](https://lnls-sirius.github.io/pydm-opi/)
----------------------------------------------------------

Requirements
------------
The lattest version of PyDM and Python>=3.6.<br>
[CONS commons](https://github.com/carneirofc/cons-common) module.<br>
Other dependencies are listed at `requerements.txt`.<br>

Install
-------
Clone from master or download the lattest release.<br>
Optionally the user may clone recursive in order to pull the module `conscommon`, if so `cd cons-common && pip install .`.<br>

Install using pip.
```
cd pydm-opi
pip3 install .
```

In order to install the `.desktop` launcher:
```
make install-files
```

Run
---
All scripts used to start the applications should be at the `bin` folder relative to the installation environment, for example:
```
~/.local/bin
/usr/local/bin
...
```

To launch the main window use the script: `sirius-hla-as-ap-conlauncher.py`

### Windows
There should be no problems running on windows.
