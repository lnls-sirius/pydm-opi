#!/usr/bin/python
from epics import caget, caput
import sys
import time
#------------------------------------------------------------------------------
'''
this script runs after every boot of BeagleBone Black. It checks whether the
pressure is lower or higher than 0.05 Torr. In case it's lower than 0.05, then
run the "process_recovery.py" script.
'''
#------------------------------------------------------------------------------
# define the PREFIX that will be used (passed as a parameter)
VBC = sys.argv[1]
#------------------------------------------------------------------------------
# read pressure value in Torr
PRESSURE = caget(VBC + ":BBB:Torr")
# if pressure is between 0.05 and 1*10**-8, trigger "process_recovery" script
if ((PRESSURE < 0.05) & (PRESSURE > 10**-8)):
    #------------------------------------------------------------------------------
    # valve names definition
    PRE_VACUUM_VALVE_SW = VBC + ":BBB:Relay1-SW"
    PRE_VACUUM_VALVE_UI = VBC + ":BBB:Relay1-UI"
    GATE_VALVE_SW = VBC + ":BBB:Relay2-SW"
    GATE_VALVE_UI = VBC + ":BBB:Relay2-UI"
    #==============================================================================
    # Stage 1:
    #==============================================================================
    caput(VBC + ":ProcessRecovery:Status1", 1)
    # turn ACP15 pump ON and wait 30 s
    caput(VBC + ":ACP:OnOff", 1)
    # set ACP15 speed to maximum (6000 rpm)
    caput(VBC + ":ACP:SpeedRPM", 6000)
    # wait until pump receives command to turn on
    while (caget(VBC + ":ACP:OnOff") == 0):
        pass
    time.sleep(30)
    #==============================================================================
    # Stage 2:
    #==============================================================================
    # open pre-vacuum valve
    caput(PRE_VACUUM_VALVE_SW, 1)


    # update UI checkbox status
    #caput(PRE_VACUUM_VALVE_UI, 1)


    # wait gate valve receives command to open
    while ( caget(PRE_VACUUM_VALVE_SW) == 0 ):
        pass
    caput(VBC + ":ProcessRecovery:Status2", 1)
    #==============================================================================
    # Stage 3:
    #==============================================================================
    # turn TURBOVAC pump ON
    caput(VBC + ":TURBOVAC:PZD1-SP.TEVL", 1)
    caput(VBC + ":TURBOVAC:PZD1-SP.ZRVL", 1)
    # wait until pump receives command to turn on
    while ( (caget(VBC + ":TURBOVAC:PZD1-SP.ZRVL") == 0) & (caget(VBC + ":TURBOVAC:PZD1-SP.TEVL") == 0) ):
        pass
    caput(VBC + ":ProcessRecovery:Status3", 1)
    #==============================================================================
    # Stage 4:
    #==============================================================================
    # wait TURBOVAC pump reaches 1200 Hz
    caput(VBC + ":TURBOVAC:PZD2-SP", 1200)
    caput(VBC + ":TURBOVAC:PZD1-SP.SXVL", 1)
    while (caget(VBC + ":TURBOVAC:PZD2-RB") < 1200):
        pass
    caput(VBC + ":TURBOVAC:PZD1-SP.SXVL", 0)
    caput(VBC + ":ProcessRecovery:Status4", 1)
    #==============================================================================
    # Stage 5:
    #==============================================================================
    # open gate valve (VAT)
    caput(GATE_VALVE_SW, 1)


    # update UI checkbox status
    #caput(GATE_VALVE_UI, 1)


    #---------------------------------------
    # read gate valve (VAT) status to check if it is really open
    loop = True
    while (loop):
        Lo = caget(VBC + ":BBB:ValveOpen")
        Lg = caget(VBC + ":BBB:ValveClosed")
        if ( Lo & (not Lg) ):
            loop = False
    caput(VBC + ":ProcessRecovery:Status5", 1)
    #==============================================================================
    caput(VBC + ":ProcessOn:Status1", 1)
    caput(VBC + ":ProcessOn:Status2", 1)
    caput(VBC + ":ProcessOn:Status3", 1)
    caput(VBC + ":ProcessOn:Status4", 1)
    caput(VBC + ":ProcessOn:Status5", 1)
