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
Optionally the user may clone recursive in order to pull the module `conscommon`., if so `cd cons-common && pip install .`.<br>

### Install using pip.
```
cd pydm-opi
pip3 install .
```
### Using [Conda](https://docs.conda.io/en/latest/miniconda.html)
```
conda create --name pydm python=3.8
conda activate pydm
pip install \
	PyQt5==5.14.2\
	numpy==1.18.4\
	pandas==1.0.3\
	pydm==1.10.0\
	pyepics==3.4.1\
	PyQt5==5.14.2\
	PyQt5-sip==12.7.2\
	pyqtgraph==0.10.0\
	python-dateutil==2.8.1\
	pytz==2020.1\
	QtPy==1.9.0\
	requests==2.23.0\
	scipy==1.4.1\
	urllib3==1.25.9\
	xlrd==1.2.0

cd ~/ && git clone --recursive https://github.com/lnls-sirius/pydm-opi && cd pydm-opi

wget https://github.com/slaclab/pydm/archive/v1.10.0.tar.gz
tar -zxvf v1.10.0.tar.gz && rm -f v1.10.0.tar.gz && cd pydm-1.10.0 && pip install . && cd ..

cd ~/pydm-opi/cons-common && pip install . && cd ../ && pip install .
```

### Desktop
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
