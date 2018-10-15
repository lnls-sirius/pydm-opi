# pydm-opi
Pydm based interfaces used in various applications. 

## Usage
It's recommended to use Python3.
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
│   └── tools
└── ui
    ├── agilent4uhv
    ├── mks937b
    └── tools
```

Inside each device folder there's a `consts.py` where the PV namming is configured. 
