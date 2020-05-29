#!/usr/bin/python
from epics import caget, caput
import sys

# ------------------------------------------------------------------------------
"""
this script do all the procedures turn off the system with full ventilation
it is divided in 6 stages, described as follow:
    -stage 1: close pre-vacuum valve (keep gate valve open)
    -stage 2: turn ACP15 and TURBOVAC pumps off
    -stage 3: wait TURBOVAC slowdown to 600 Hz
    -stage 4: open X203 (TURBOVAC venting valve)
    -stage 5: wait pressure decrease to 760 Torr
    -stage 6: close X203 and gate valves
"""
print("======================")
print("Script: process_off.py")
print("======================")
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
caput(VBC + ":ProcessOffFV:Status1", 0)
caput(VBC + ":ProcessOffFV:Status2", 0)
caput(VBC + ":ProcessOffFV:Status3", 0)
caput(VBC + ":ProcessOffFV:Status4", 0)
caput(VBC + ":ProcessOffFV:Status5", 0)
caput(VBC + ":ProcessOffFV:Status6", 0)
# ==============================================================================
# Stage 1:
# ==============================================================================
# close pre-vacuum valve (and keeps gate valve open)
caput(PRE_VACUUM_VALVE_SW, 0)


# update UI checkbox status
# caput(PRE_VACUUM_VALVE_UI, 0)


# wait until valve receives command to open
while caget(PRE_VACUUM_VALVE_SW):
    pass
caput(VBC + ":ProcessOffFV:Status1", 1)
# ==============================================================================
# Stage 2:
# ==============================================================================
# change venting valve to manual control
caput(VBC + ":TURBOVAC:AK-SP", 0)
caput(VBC + ":TURBOVAC:PNU-SP", 134)
caput(VBC + ":TURBOVAC:IND-SP", 2)
caput(VBC + ":TURBOVAC:PWE-SP", 18)
caput(VBC + ":TURBOVAC:AK-SP", 7)

# turn TURBOVAC and ACP15 pumps OFF
caput(VBC + ":TURBOVAC:PZD1-SP.ZRVL", 0)
caput(VBC + ":ACP:OnOff", 0)
# wait until pump receives command to turn off
while caget(VBC + ":ACP:OnOff"):
    pass
caput(VBC + ":ProcessOffFV:Status2", 1)
# ==============================================================================
# Stage 3:
# ==============================================================================
# wait until TURBOVAC frequency decrease to 600 Hz
while caget(VBC + ":TURBOVAC:PZD2-RB") > caget(VBC + ":SYSTEM:OffFrequency"):
    pass
caput(VBC + ":ProcessOffFV:Status3", 1)
# ==============================================================================
# Stage 4:
# ==============================================================================
# open X203 valve (TURBOVAC venting valve)
caput(VBC + ":TURBOVAC:VentingValve-SW", 1)
# update UI checkbox status
caput(VBC + ":TURBOVAC:VentingValve-UI", 1)
# wait until venting valve receives command to close
while caget(VBC + ":TURBOVAC:VentingValve-SW") == 0:
    pass
caput(VBC + ":ProcessOffFV:Status4", 1)
# ==============================================================================
# Stage 5:
# ==============================================================================
# wait until pressure gets 760 Torr
while caget(VBC + ":BBB:Torr") < (
    caget(VBC + ":SYSTEM:OffPressureBase") * 10 ** caget(VBC + ":SYSTEM:OffPressureExp")
):
    pass
caput(VBC + ":ProcessOffFV:Status5", 1)
# ==============================================================================
# Stage 6:
# ==============================================================================
# close all the valves (gate valve is already closed)
caput(PRE_VACUUM_VALVE_SW, 0)
caput(VBC + ":TURBOVAC:VentingValve-SW", 0)  # close X203
# update UI checkbox status
caput(PRE_VACUUM_VALVE_UI, 0)
caput(VBC + ":TURBOVAC:VentingValve-UI", 0)  # close X203
# wait until venting valve receives command to close
while caget(PRE_VACUUM_VALVE_SW):
    pass
caput(VBC + ":ProcessOffFV:Status6", 1)
# ==============================================================================
# complement value of PV to launch "Process Finished" window
# caput(VBC + ":Process:Bool", not(caget(VBC + ":Process:Bool")))
caput(VBC + ":Process:Bool", 1)
caput(VBC + ":Process:Bool", 0)
# ==============================================================================
