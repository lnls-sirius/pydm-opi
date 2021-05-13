#!/usr/bin/python
from epics import caget, caput
import sys

# ------------------------------------------------------------------------------
"""
this script do all the procedures to decrease the pressure of the system
it is divided in 5 stages, described as follow:
    -stage 1: open gate and pre-vacuum valves (and wait gate valve really closes)
    -stage 2: wait until gate valve actually closes
    -stage 3: turn ACP15 on
    -stage 4: wait pressure decrease to less than 0.05 Torr
    -stage 5: turn TURBOVAC on
"""
print("=====================")
print("Script: process_on.py")
print("=====================")
# ------------------------------------------------------------------------------
# define the PREFIX that will be used (passed as a parameter)
VBC = sys.argv[1]
# ------------------------------------------------------------------------------
# valve names definition
PRE_VACUUM_VALVE_SW = VBC + ":BBB:Relay1-SW"
PRE_VACUUM_VALVE_UI = VBC + ":BBB:Relay1-UI"
GATE_VALVE_SW = VBC + ":BBB:Relay2-SW"
GATE_VALVE_UI = VBC + ":BBB:Relay2-UI"
# ------------------------------------------------------------------------------
# clear all status PVs
caput(VBC + ":ProcessOn:Status1", 0)
caput(VBC + ":ProcessOn:Status2", 0)
caput(VBC + ":ProcessOn:Status3", 0)
caput(VBC + ":ProcessOn:Status4", 0)
caput(VBC + ":ProcessOn:Status5", 0)
# ==============================================================================
# Stage 1:
# ==============================================================================
# wait TURBOVAC pump stops completely
caput(VBC + ":ProcessOn:Status1", 1)
while caget(VBC + ":TURBOVAC:PZD2-RB") != 0:
    pass
# ==============================================================================
# Stage 2:
# ==============================================================================
# open gate valve (VAT) and the pre-vacuum valve
caput(GATE_VALVE_SW, 1)
caput(PRE_VACUUM_VALVE_SW, 1)


# update UI checkbox status
# caput(GATE_VALVE_UI, 1)
# caput(PRE_VACUUM_VALVE_UI, 1)


# ---------------------------------------
# wait gate valve receives command to open
while caget(PRE_VACUUM_VALVE_SW) == 0:
    pass
# read gate valve (VAT) status to check if it is really open
loop = True
while loop:
    Lo = caget(VBC + ":BBB:ValveOpen")
    Lg = caget(VBC + ":BBB:ValveClosed")
    if Lo & (not (Lg)):
        loop = False
caput(VBC + ":ProcessOn:Status2", 1)
# ==============================================================================
# Stage 3:
# ==============================================================================
# turn ACP15 pump ON
caput(VBC + ":ACP:OnOff", 1)
# wait until pump receives command to turn on
while caget(VBC + ":ACP:OnOff") == 0:
    pass
caput(VBC + ":ProcessOn:Status3", 1)
# ==============================================================================
# Stage 4:
# ==============================================================================
# read the pressure and proceed when its value is under 5*(10^-2) Torr
while caget(VBC + ":BBB:Torr") > (
    caget(VBC + ":SYSTEM:OnPressureBase") * 10 ** caget(VBC + ":SYSTEM:OnPressureExp")
):
    pass
caput(VBC + ":ProcessOn:Status4", 1)
# ==============================================================================
# Stage 5:
# ==============================================================================
# turn TURBOVAC pump ON
caput(VBC + ":TURBOVAC:PZD1-SP.TEVL", 1)
caput(VBC + ":TURBOVAC:PZD1-SP.ZRVL", 1)
# wait until pump receives command to turn on
while (caget(VBC + ":TURBOVAC:PZD1-SP.ZRVL") == 0) & (
    caget(VBC + ":TURBOVAC:PZD1-SP.TEVL") == 0
):
    pass
caput(VBC + ":ProcessOn:Status5", 1)
# ==============================================================================
# complement value of PV to launch "Process Finished" window
# caput(VBC + ":Process:Bool", not(caget(VBC + ":Process:Bool")))
caput(VBC + ":Process:Bool", 1)
caput(VBC + ":Process:Bool", 0)
# ==============================================================================
