import epics


def _clear_status(prefix: str):
    # clear all status PVs
    epics.caput(f"{prefix}:ProcessOn:Status1", 0)
    epics.caput(f"{prefix}:ProcessOn:Status2", 0)
    epics.caput(f"{prefix}:ProcessOn:Status3", 0)
    epics.caput(f"{prefix}:ProcessOn:Status4", 0)
    epics.caput(f"{prefix}:ProcessOn:Status5", 0)
    # clear all status PVs for "Off Process"
    epics.caput(f"{prefix}:ProcessOffFV:Status1", 0)
    epics.caput(f"{prefix}:ProcessOffFV:Status2", 0)
    epics.caput(f"{prefix}:ProcessOffFV:Status3", 0)
    epics.caput(f"{prefix}:ProcessOffFV:Status4", 0)
    epics.caput(f"{prefix}:ProcessOffFV:Status5", 0)
    epics.caput(f"{prefix}:ProcessOffFV:Status6", 0)


def _stage_1(prefix: str):
    """wait TURBOVAC pump stops completely"""
    epics.caput(f"{prefix}:ProcessOn:Status1", 1)
    while epics.caget(f"{prefix}:TURBOVAC:PZD2-RB") != 0:
        pass


def _stage_2(prefix: str):
    """Stage 2:"""
    PRE_VACUUM_VALVE_SW = f"{prefix}:BBB:Relay1-SW"
    GATE_VALVE_SW = f"{prefix}:BBB:Relay2-SW"
    # open gate valve (VAT) and the pre-vacuum valve
    epics.caput(GATE_VALVE_SW, 1)
    epics.caput(PRE_VACUUM_VALVE_SW, 1)

    # update UI checkbox status
    # epics.caput(GATE_VALVE_UI, 1)
    # epics.caput(PRE_VACUUM_VALVE_UI, 1)

    # ---------------------------------------
    # wait gate valve receives command to open
    while epics.caget(PRE_VACUUM_VALVE_SW) == 0:
        pass
    # read gate valve (VAT) status to check if it is really open
    loop = True
    while loop:
        Lo = epics.caget(f"{prefix}:BBB:ValveOpen")
        Lg = epics.caget(f"{prefix}:BBB:ValveClosed")
        if Lo & (not (Lg)):
            loop = False
    epics.caput(f"{prefix}:ProcessOn:Status2", 1)


def _stage_3(prefix: str):
    """Stage 3:"""
    # turn ACP15 pump ON
    epics.caput(f"{prefix}:ACP:OnOff", 1)
    # wait until pump receives command to turn on
    while epics.caget(f"{prefix}:ACP:OnOff") == 0:
        pass
    epics.caput(f"{prefix}:ProcessOn:Status3", 1)


def _stage_4(prefix: str):
    """Stage 4:"""
    # read the pressure and proceed when its value is under 5*(10^-2) Torr
    while epics.caget(f"{prefix}:BBB:Torr") > (
        epics.caget(f"{prefix}:SYSTEM:OnPressureBase")
        * 10 ** epics.caget(f"{prefix}:SYSTEM:OnPressureExp")
    ):
        pass
    epics.caput(f"{prefix}:ProcessOn:Status4", 1)


def _stage_5(prefix: str):
    """Stage 5:"""
    # turn TURBOVAC pump ON
    epics.caput(f"{prefix}:TURBOVAC:PZD1-SP.TEVL", 1)
    epics.caput(f"{prefix}:TURBOVAC:PZD1-SP.ZRVL", 1)
    # wait until pump receives command to turn on
    while (epics.caget(f"{prefix}:TURBOVAC:PZD1-SP.ZRVL") == 0) & (
        epics.caget(f"{prefix}:TURBOVAC:PZD1-SP.TEVL") == 0
    ):
        pass
    epics.caput(f"{prefix}:ProcessOn:Status5", 1)
    # ==============================================================================
    # complement value of PV to launch "Process Finished" window
    # epics.caput(VBC + ":Process:Bool", not(epics.caget(VBC + ":Process:Bool")))
    epics.caput(f"{prefix}:ProcessOn:Bool", 1)
    epics.caput(f"{prefix}:ProcessOn:Bool", 0)
    # ==============================================================================


def process_on(prefix: str):
    """
    this script do all the procedures to decrease the pressure of the system
    it is divided in 5 stages, described as follow:
        -stage 1: open gate and pre-vacuum valves (and wait gate valve really closes)
        -stage 2: wait until gate valve actually closes
        -stage 3: turn ACP15 on
        -stage 4: wait pressure decrease to less than 0.05 Torr
        -stage 5: turn TURBOVAC on
    """
    _clear_status(prefix=prefix)
    _stage_1(prefix=prefix)
    _stage_2(prefix=prefix)
    _stage_3(prefix=prefix)
    _stage_4(prefix=prefix)
    _stage_5(prefix=prefix)
