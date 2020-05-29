#!/usr/bin/python
from epics import caput
import sys

# ------------------------------------------------------------------------------
"""
this script clean all the status PV for both On/Off Process
"""
# ------------------------------------------------------------------------------
print("==========================")
print("Script: clean_status_PV.py")
print("==========================")
# define the PREFIX that will be used (passed as a parameter)
VBC = sys.argv[1]
# -----------------------------------------------
# clear all status PVs for "On Process"
caput(VBC + ":ProcessOn:Status1", 0)
caput(VBC + ":ProcessOn:Status2", 0)
caput(VBC + ":ProcessOn:Status3", 0)
caput(VBC + ":ProcessOn:Status4", 0)
caput(VBC + ":ProcessOn:Status5", 0)
# -----------------------------------------------
# clear all status PVs for "Off Process"
caput(VBC + ":ProcessOffFV:Status1", 0)
caput(VBC + ":ProcessOffFV:Status2", 0)
caput(VBC + ":ProcessOffFV:Status3", 0)
caput(VBC + ":ProcessOffFV:Status4", 0)
caput(VBC + ":ProcessOffFV:Status5", 0)
caput(VBC + ":ProcessOffFV:Status6", 0)
# -----------------------------------------------
# clear all status PVs for "recovering from pressurized system" process (5*10^-2 ~ 1*10^-8)
caput(VBC + ":ProcessRecovery:Status1", 0)
caput(VBC + ":ProcessRecovery:Status2", 0)
caput(VBC + ":ProcessRecovery:Status3", 0)
caput(VBC + ":ProcessRecovery:Status4", 0)
caput(VBC + ":ProcessRecovery:Status5", 0)
# ------------------------------------------------------------------------------
