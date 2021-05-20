import epics
import time


def _clear_status(prefix: str):
    # ------------------------------------------------------------------------------
    # clear all status PVs
    epics.caput(f"{prefix}:ProcessRecovery:Status1", 0)
    epics.caput(f"{prefix}:ProcessRecovery:Status2", 0)
    epics.caput(f"{prefix}:ProcessRecovery:Status3", 0)
    epics.caput(f"{prefix}:ProcessRecovery:Status4", 0)
    epics.caput(f"{prefix}:ProcessRecovery:Status5", 0)


def _stage_1(prefix: str):
    """Stage 1:"""
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
    """Stage 2:"""
    PRE_VACUUM_VALVE_SW = f"{prefix}:BBB:Relay1-SW"
    # open pre-vacuum valve
    epics.caput(PRE_VACUUM_VALVE_SW, 1)

    # update UI checkbox status
    # epics.caput(PRE_VACUUM_VALVE_UI, 1)

    # wait pre-vacuum valve receives value to open
    while epics.caget(PRE_VACUUM_VALVE_SW) == 0:
        pass
    epics.caput(f"{prefix}:ProcessRecovery:Status2", 1)
    pass


def _stage_3(prefix: str):
    """Stage 3:"""
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
    """Stage 4:"""
    # wait TURBOVAC pump reaches 1200 Hz
    epics.caput(f"{prefix}:TURBOVAC:PZD2-SP", 1200)
    epics.caput(f"{prefix}:TURBOVAC:PZD1-SP.SXVL", 1)
    while epics.caget(f"{prefix}:TURBOVAC:PZD2-RB") < 1200:
        pass
    epics.caput(f"{prefix}:TURBOVAC:PZD1-SP.SXVL", 0)
    epics.caput(f"{prefix}:ProcessRecovery:Status4", 1)


def _stage_5(prefix: str):
    """Stage 5:"""
    GATE_VALVE_SW = f"{prefix}:BBB:Relay2-SW"
    # open gate valve (VAT)
    epics.caput(GATE_VALVE_SW, 1)

    # update UI checkbox status
    # epics.caput(GATE_VALVE_UI, 1)

    # ---------------------------------------
    # read gate valve (VAT) status to check if it is really open
    loop = True
    while loop:
        Lo = epics.caget(f"{prefix}:BBB:ValveOpen")
        Lg = epics.caget(f"{prefix}:BBB:ValveClosed")
        if Lo & (not Lg):
            loop = False
    epics.caput(f"{prefix}:ProcessRecovery:Status5", 1)
    # ==============================================================================
    # complement value of PV to launch "Process Finished" window
    # epics.caput(VBC + ":Process:Bool", not(epics.caget(VBC + ":Process:Bool")))
    epics.caput(f"{prefix}:ProcessRec:Bool", 1)
    epics.caput(f"{prefix}:ProcessRec:Bool", 0)
    # ==============================================================================


def process_recovery(prefix: str):
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
    _clear_status(prefix=prefix)
    _stage_1(prefix=prefix)
    _stage_2(prefix=prefix)
    _stage_3(prefix=prefix)
    _stage_4(prefix=prefix)
    _stage_5(prefix=prefix)
