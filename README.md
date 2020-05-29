CONS OPIs
===========

This repo should contain every PyDM OPI developed by the CONS group currently in use.

[Read the docs !](https://lnls-sirius.github.io/pydm-opi/)
----------------------------------------------------------

Requirements
------------
The lattest version of PyDM and Python>=3.6.<br>
[CONS commons](https://github.com/lnls-sirius/cons-common) module.<br>
Other dependencies are listed at `requerements.txt`.<br>

Install
-------
This repository depends on [PyDM](https://github.com/slaclab/pydm),
[PyEPICS](https://github.com/pyepics/pyepics), [CONS Common](https://github.com/lnls-sirius/cons-common) and Python>=3.6 .

Clone from master or download the lattest release.<br>
Optionally the user may clone recursive in order to pull the module `conscommon`. If so, install the module using `cd cons-common && pip install .`.<br>

### Using [Conda](https://docs.conda.io/en/latest/miniconda.html)
This is the recommended way to install ...

Install EPICS and add it to PATH(Windows only)
```
https://epics.anl.gov/download/distributions/EPICSWindowsTools1.44-x64.msi
```

Create and activate the conda environment:
```
conda init <shell name> # Restart shell after ... (bash, powershell, etc...)
conda create --name pydm python=3.7 # pyqtgraph==0.1.0 does not work with python 3.8
conda activate pydm
```

Install dependencies and OPIs (Will use ~/ as the default path but feel free to change):
```
# Install PyDM (If on Windows `wget` and `tar` may not be available, just download the file using a browser and extract it)
wget https://github.com/slaclab/pydm/archive/v1.10.1.tar.gz
tar -zxvf v1.10.1.tar.gz && rm -f v1.10.1.tar.gz && cd pydm-1.10.1 && pip install . && cd ..

# Install pydm-opi and cons-common
cd ~/ && git clone --recursive https://github.com/lnls-sirius/pydm-opi && cd pydm-opi
cd ~/pydm-opi/cons-common && pip install . && cd ../ && pip install .
```

### Desktop
In order to install the `.desktop` launcher:
```
make install-files
```
If using conda, remember to fix the Exec entry at the `.desktop' file accordingly:
``` 
/bin/bash -c 'source ~/miniconda3/etc/profile.d/conda.sh && conda activate pydm && sirius-hla-as-ap-conlauncher.py'
```

Run
---
All scripts used to start the applications should be at the `bin` folder relative to the python installation environment, for example:
```
~/.local/bin
/usr/local/bin
...
```

To launch the main window use the script: `sirius-hla-as-ap-conlauncher.py`

### Windows
There should be no problems running on windows.
