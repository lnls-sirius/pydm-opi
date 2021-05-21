import time

import epics


def _stage_1(prefix: str):
    epics.caput(f"{prefix}:ProcessRecovery:Status1", 1)
    # turn ACP15 pump ON and wait 30 s
    epics.caput(f"{prefix}:ACP:OnOff", 1)
    # set ACP15 speed to maximum (6000 rpm)
    epics.caput(f"{prefix}:ACP:SpeedRPM", 6000)
    # wait until pump receives command to turn on
    while epics.caget(f"{prefix}:ACP:OnOff") == 0:
        pass
    time.sleep(30)


def _stage_2(prefix: str):
    PRE_VACUUM_VALVE_SW = f"{prefix}:BBB:Relay1-SW"
    # open pre-vacuum valve
    epics.caput(PRE_VACUUM_VALVE_SW, 1)

    # wait gate valve receives command to open
    while epics.caget(PRE_VACUUM_VALVE_SW) == 0:
        pass
    epics.caput(f"{prefix}:ProcessRecovery:Status2", 1)


def _stage_3(prefix: str):
    # turn TURBOVAC pump ON
    epics.caput(f"{prefix}:TURBOVAC:PZD1-SP.TEVL", 1)
    epics.caput(f"{prefix}:TURBOVAC:PZD1-SP.ZRVL", 1)
    # wait until pump receives command to turn on
    while (epics.caget(f"{prefix}:TURBOVAC:PZD1-SP.ZRVL") == 0) & (
        epics.caget(f"{prefix}:TURBOVAC:PZD1-SP.TEVL") == 0
    ):
        pass
    epics.caput(f"{prefix}:ProcessRecovery:Status3", 1)


def _stage_4(prefix: str):
    # wait TURBOVAC pump reaches 1200 Hz
    epics.caput(f"{prefix}:TURBOVAC:PZD2-SP", 1200)
    epics.caput(f"{prefix}:TURBOVAC:PZD1-SP.SXVL", 1)
    while epics.caget(f"{prefix}:TURBOVAC:PZD2-RB") < 1200:
        pass
    epics.caput(f"{prefix}:TURBOVAC:PZD1-SP.SXVL", 0)
    epics.caput(f"{prefix}:ProcessRecovery:Status4", 1)


def _stage_5(prefix: str):
    GATE_VALVE_SW = f"{prefix}:BBB:Relay2-SW"
    # open gate valve (VAT)
    epics.caput(GATE_VALVE_SW, 1)

    # ---------------------------------------
    # read gate valve (VAT) status to check if it is really open
    loop = True
    while loop:
        Lo = epics.caget(f"{prefix}:BBB:ValveOpen")
        Lg = epics.caget(f"{prefix}:BBB:ValveClosed")
        if Lo & (not Lg):
            loop = False
    epics.caput(f"{prefix}:ProcessRecovery:Status5", 1)

    epics.caput(f"{prefix}:ProcessOn:Status1", 1)
    epics.caput(f"{prefix}:ProcessOn:Status2", 1)
    epics.caput(f"{prefix}:ProcessOn:Status3", 1)
    epics.caput(f"{prefix}:ProcessOn:Status4", 1)
    epics.caput(f"{prefix}:ProcessOn:Status5", 1)


def initialization(prefix: str):
    """
    this script runs after every boot of BeagleBone Black. It checks whether the
    pressure is lower or higher than 0.05 Torr. In case it's lower than 0.05, then
    run the "process_recovery.py" script.
    """
    # ------------------------------------------------------------------------------
    # read pressure value in Torr
    PRESSURE = epics.caget(f"{prefix}:BBB:Torr")
    # if pressure is between 0.05 and 1*10**-8, trigger "process_recovery" script
    if (PRESSURE < 0.05) & (PRESSURE > 10 ** -8):
        _stage_1(prefix=prefix)
        _stage_2(prefix=prefix)
        _stage_3(prefix=prefix)
        _stage_4(prefix=prefix)
        _stage_5(prefix=prefix)
