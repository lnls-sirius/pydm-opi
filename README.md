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
pandas==0.23.4
xlrd==1.1.0
```

## Usage 
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

Python code placed inside `./src/` folder.
Qt Designer .ui files inside `./ui/` folder.
Images and .qrc files inside `./images/` folder.

When moving files around or changing names, it's necessary to update the correspondiong entry at:
```
./src/paths.py
```
