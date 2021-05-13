#!/usr/bin/python
from epics import caget, caput
import sys
import time

# ------------------------------------------------------------------------------
"""
this script do all the procedures to recover from a pressurized system (after a
power failure, for example) if the pressure is in the range (5*10^-2 ~ 1*10^-8).
It is divided in 5 stages, described as follow:
    -stage 1: turn ACP15 on and wait 30 s
    -stage 2: open pre-vacuum valve
    -stage 3: turn TURBOVAC on
    -stage 4: wait TURBOVAC frequency reaches 1200 Hz
    -stage 5: open gate valve
"""
print("===========================")
print("Script: process_recovery.py")
print("===========================")
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
caput(VBC + ":ProcessRecovery:Status1", 0)
caput(VBC + ":ProcessRecovery:Status2", 0)
caput(VBC + ":ProcessRecovery:Status3", 0)
caput(VBC + ":ProcessRecovery:Status4", 0)
caput(VBC + ":ProcessRecovery:Status5", 0)
caput(VBC + ":ProcessRecovery:Status6", 0)
# ==============================================================================
# Stage 1:
# ==============================================================================
caput(VBC + ":ProcessRecovery:Status1", 1)
# turn ACP15 pump ON and wait 30 s
caput(VBC + ":ACP:OnOff", 1)
# set ACP15 speed to maximum (6000 rpm)
caput(VBC + ":ACP:SpeedRPM", 6000)
# wait until pump receives command to turn on
while caget(VBC + ":ACP:OnOff") == 0:
    pass
time.sleep(30)
# ==============================================================================
# Stage 2:
# ==============================================================================
# open pre-vacuum valve
caput(PRE_VACUUM_VALVE_SW, 1)


# update UI checkbox status
# caput(PRE_VACUUM_VALVE_UI, 1)


# wait gate valve receives command to open
while caget(PRE_VACUUM_VALVE_SW) == 0:
    pass
caput(VBC + ":ProcessRecovery:Status2", 1)
# ==============================================================================
# Stage 3:
# ==============================================================================
# turn TURBOVAC pump ON
caput(VBC + ":TURBOVAC:PZD1-SP.TEVL", 1)
caput(VBC + ":TURBOVAC:PZD1-SP.ZRVL", 1)
# wait until pump receives command to turn on
while (caget(VBC + ":TURBOVAC:PZD1-SP.ZRVL") == 0) & (
    caget(VBC + ":TURBOVAC:PZD1-SP.TEVL") == 0
):
    pass
caput(VBC + ":ProcessRecovery:Status3", 1)
# ==============================================================================
# Stage 4:
# ==============================================================================
# wait TURBOVAC pump reaches 1200 Hz
caput(VBC + ":TURBOVAC:PZD2-SP", 1200)
caput(VBC + ":TURBOVAC:PZD1-SP.SXVL", 1)
while caget(VBC + ":TURBOVAC:PZD2-RB") < 1200:
    pass
caput(VBC + ":TURBOVAC:PZD1-SP.SXVL", 0)
caput(VBC + ":ProcessRecovery:Status4", 1)
# ==============================================================================
# Stage 5:
# ==============================================================================
# open gate valve (VAT)
caput(GATE_VALVE_SW, 1)


# update UI checkbox status
# caput(GATE_VALVE_UI, 1)


# ---------------------------------------
# read gate valve (VAT) status to check if it is really open
loop = True
while loop:
    Lo = caget(VBC + ":BBB:ValveOpen")
    Lg = caget(VBC + ":BBB:ValveClosed")
    if Lo & (not Lg):
        loop = False
caput(VBC + ":ProcessRecovery:Status5", 1)
# ==============================================================================
# complement value of PV to launch "Process Finished" window
# caput(VBC + ":Process:Bool", not(caget(VBC + ":Process:Bool")))
caput(VBC + ":Process:RecBool", 1)
caput(VBC + ":Process:RecBool", 0)
# ==============================================================================
