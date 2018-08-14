

pydm --hide-nav-bar --hide-menu-bar --hide-status-bar -m '{"DEVICE" : "VGC1", "A":"CC", "B":"CC", "C":"PR"}' info.ui &
pydm --hide-nav-bar --hide-menu-bar --hide-status-bar -m '{"DEVICE" : "VGC1", "r1":"1","r2":"2","r3":"3","r4":"4","GAUGE":"A1", "channel":"1"}' cc.ui &
pydm --hide-nav-bar --hide-menu-bar --hide-status-bar -m '{"DEVICE" : "VGC1", "r1":"5","r2":"6","r3":"7","r4":"8","GAUGE":"B1", "channel":"3"}' cc.ui &
pydm --hide-nav-bar --hide-menu-bar --hide-status-bar -m '{"DEVICE" : "VGC1", "r1":"9","r2":"10","r3":"11","r4":"12","GAUGE_1":"C1", "GAUGE_2":"C2", "channel_1":"5", "channel_2":"6"}' pirani.ui &
pydm --hide-nav-bar --hide-menu-bar --hide-status-bar -m '{"DEVICE" : "VGC1"}' pressure.ui &

#  --hide-nav-bar        Start PyDM with the navigation bar hidden.
#  --hide-menu-bar       Start PyDM with the menu bar hidden.
#  --hide-status-bar     Start PyDM with the status bar hidden.
#  --read-only           Start PyDM in a Read-Only mode.

