export EPICS_CA_SERVER_PORT=5072
pydm --hide-nav-bar --hide-menu-bar  --hide-status-bar -m '{"DEVICE":"Ag", "PREFIX_C1":"Ag:Ch1", "PREFIX_C2":"Ag:Ch2", "PREFIX_C3":"Ag:Ch3", "PREFIX_C4":"CH4"}'  device_main.ui 
