#!/usr/bin/python
from epics import caget, caput
import sys

# ------------------------------------------------------------------------------
"""
this script runs after the user hits the "ON" button under the "system_tab.ui"
window. It checks whether the pressure is lower or higher than 0.05 Torr.
 - if its value is lower than 0.05, then the "process_on" script is executed
 - if its value is higher, then the "system_pressurized" window will pop-up
"""
print("=========================")
print("Script: check_pressure.py")
print("=========================")
# ------------------------------------------------------------------------------
# define the PREFIX that will be used (passed as a parameter)
VBC = sys.argv[1]
FIRST_TIME = sys.argv[2]
# ------------------------------------------------------------------------------
# read pressure value in Torr
PRESSURE = caget(VBC + ":BBB:Torr")
# update pressure value displayed in "system_pressurized.ui" window
caput(VBC + ":BBB:TorrBaseMsg", caget(VBC + ":BBB:TorrBase"))
caput(VBC + ":BBB:TorrExpMsg", caget(VBC + ":BBB:TorrExp"))
# update value showed in "system_pressurized.ui" window
# if pressure value is bigger than 0.05 Torr, trigger "process_on" script
if PRESSURE > 0.05:
    if FIRST_TIME == "0":
        # caput(VBC + ":Process:TriggerOn", not(caget(VBC + ":ProcessRecovery:TriggerOn")))
        caput(VBC + ":Process:TriggerOn", 1)
        caput(VBC + ":Process:TriggerOn", 0)
    elif FIRST_TIME == "1":
        pass
# if pressure is between 0.05 and 1*10**-8, trigger "process_recovery" script
elif (PRESSURE < 0.05) & (PRESSURE > 10 ** -8):
    caput(VBC + ":Process:TriggerPressurized", 1)
    caput(VBC + ":Process:TriggerPressurized", 0)
# ==============================================================================
