# CONS OPIs
This repo should contain every PyDM OPI developed by the CONS group currently in use.

### directory structure
```
.
├── miscellaneous
│   └── windows
├── scripts
└── siriushlacon
    ├── agilent4uhv
    │   └── ui
    .
    .
    .
    ├── tools
    └── utils
        ├── css
        ├── images
        └── ui
```

## Requirements
The lattest version of PyDM and Python>=3.6. Other dependencies are listed at `requerements.txt`.

## Install
Clone from master or download the lattest release. Install using pip.
```
cd pydm-opi
pip3 install .
```
In order to install the `.desktop` launcher:
```
make install
```
### Windows
The user should use miniconda and install everything there !
[Miniconda](https://gitlab.cnpem.br/con/pydm-installer)


## Run
All scripts used to start the applications should be at the `bin` folder relative to the installation environment.
```
~/.local/bin
/usr/local/bin
...
```

To launch the main window use the script: `sirius-hla-as-ap-conlauncher.py`

### Windows
There should be no problems running on windows.
