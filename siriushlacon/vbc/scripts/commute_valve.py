#!/usr/bin/python
from epics import caget, caput
import time
import sys

# ------------------------------------------------------------------------------
"""
this is script is used to commute a valve value
"""
print("========================")
print("Script: commute_valve.py")
print("========================")
# ------------------------------------------------------------------------------
# define the PREFIX that will be used (passed as a parameter)
VBC = sys.argv[1]
VALVE = sys.argv[2]
SW = VBC + ":BBB:Relay" + VALVE + "-SW"
UI = VBC + ":BBB:Relay" + VALVE + "-UI"
# ------------------------------------------------------------------------------
time.sleep(1)
# if relay swtiching message is confirmed, change PV SW values:
if str(sys.argv[3]) == "yes":
    if VALVE == "1":
        caput(SW, not (caget(SW)))
    elif VALVE == "2":
        caput(SW, not (caget(SW)))
    elif VALVE == "3":
        caput(SW, not (caget(SW)))
    elif VALVE == "4":
        caput(SW, not (caget(SW)))
    elif VALVE == "5":
        caput(
            VBC + ":TURBOVAC:VentingValve-SW",
            not (caget(VBC + ":TURBOVAC:VentingValve-SW")),
        )
# if relay swtiching message is canceled, do nothing:
elif sys.argv[3] == "no":
    if VALVE == "1":
        caput(UI + ".RVAL", caget(SW))
    elif VALVE == "2":
        caput(UI + ".RVAL", caget(SW))
    elif VALVE == "3":
        caput(UI + ".RVAL", caget(SW))
    elif VALVE == "4":
        caput(UI + ".RVAL", caget(SW))
    elif VALVE == "5":
        caput(
            VBC + ":TURBOVAC:VentingValve-UI.RVAL",
            caget(VBC + ":TURBOVAC:VentingValve-SW"),
        )
