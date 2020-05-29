#!/usr/bin/python
from epics import caget, caput
import sys
#------------------------------------------------------------------------------
'''
this script clean all the status PV for both On/Off Process
'''
#------------------------------------------------------------------------------
# define the PREFIX that will be used (passed as a parameter)
VBC = sys.argv[1]
finished = sys.argv[2]
#-----------------------------------------------
# called after ON process is finished
if (finished == "ON"):
    # clear all status PVs for "Off Process"
    caput(VBC + ":ProcessOffFV:Status1", 0)
    caput(VBC + ":ProcessOffFV:Status2", 0)
    caput(VBC + ":ProcessOffFV:Status3", 0)
    caput(VBC + ":ProcessOffFV:Status4", 0)
    caput(VBC + ":ProcessOffFV:Status5", 0)
    caput(VBC + ":ProcessOffFV:Status6", 0)
    # clear all status PVs for "Recovery Process"
    caput(VBC + ":ProcessRecovery:Status1", 0)
    caput(VBC + ":ProcessRecovery:Status2", 0)
    caput(VBC + ":ProcessRecovery:Status3", 0)
    caput(VBC + ":ProcessRecovery:Status4", 0)
    caput(VBC + ":ProcessRecovery:Status5", 0)
#-----------------------------------------------
# called after OFF process is finished
elif (finished == "OFF"):
    # clear all status PVs for "On Process"
    caput(VBC + ":ProcessOn:Status1", 0)
    caput(VBC + ":ProcessOn:Status2", 0)
    caput(VBC + ":ProcessOn:Status3", 0)
    caput(VBC + ":ProcessOn:Status4", 0)
    caput(VBC + ":ProcessOn:Status5", 0)
    # clear all status PVs for "Recovery Process"
    caput(VBC + ":ProcessRecovery:Status1", 0)
    caput(VBC + ":ProcessRecovery:Status2", 0)
    caput(VBC + ":ProcessRecovery:Status3", 0)
    caput(VBC + ":ProcessRecovery:Status4", 0)
    caput(VBC + ":ProcessRecovery:Status5", 0)
#-----------------------------------------------
# called after REC process is finished
elif (finished == "REC"):
    # clear all status PVs for "recovering from pressurized system" process (5*10^-2 ~ 1*10^-8)
    caput(VBC + ":ProcessOn:Status1", 1)
    caput(VBC + ":ProcessOn:Status2", 1)
    caput(VBC + ":ProcessOn:Status3", 1)
    caput(VBC + ":ProcessOn:Status4", 1)
    caput(VBC + ":ProcessOn:Status5", 1)
    # clear all status PVs for "Off Process"
    caput(VBC + ":ProcessOffFV:Status1", 0)
    caput(VBC + ":ProcessOffFV:Status2", 0)
    caput(VBC + ":ProcessOffFV:Status3", 0)
    caput(VBC + ":ProcessOffFV:Status4", 0)
    caput(VBC + ":ProcessOffFV:Status5", 0)
    caput(VBC + ":ProcessOffFV:Status6", 0)
#------------------------------------------------------------------------------
