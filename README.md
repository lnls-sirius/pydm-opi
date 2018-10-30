# Pydm OPI
Pydm based interfaces used in various applications. 

## Dependencies
It's recommended to use Python3.<br>
Tested using:
```
Python 3.6.5.
PyQt5==5.9.2
PyQt5-sip==4.19.12
pyqtgraph==0.10.0
pydm==1.4.2+3.gb6dd133
```

## Usage
Inside `launch.sh` the user should set the ip/port where the PV Gateway is running. This is done by editing:
```
# PV Gateway Address
export EPICS_CA_ADDR_LIST=127.0.0.1:5072
```
After that, simply run:
```
./launch.sh
```

## Maintenance
Currently the project is structured as:
```
.
├── images
├── src
│   ├── agilent4uhv
│   ├── mks937b
│   ├── ...
│   └── tools
└── ui
    ├── agilent4uhv
    ├── mks937b
    ├── ...
    └── tools

Python code is to be placed inside `./src/` folder.
Qt Designer .ui files inside `./ui/` folder.
Images and .qrc files inside `./images/` folder.
```
Inside each device folder there's a `consts.py` file where the PV namming is configured. If the user wishes to change/add a pv name it's necessary to edit the file at:<br>
```
./src/<device-name>/consts.py
```

When moving files around or changing names, it's necessary to update the correspondiong entry at:
```
./src/paths.py
```