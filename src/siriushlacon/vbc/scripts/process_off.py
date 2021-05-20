import epics


def _clear_pvs(prefix: str):
    # clear all status PVs
    epics.caput(f"{prefix}:ProcessOffFV:Status1", 0)
    epics.caput(f"{prefix}:ProcessOffFV:Status2", 0)
    epics.caput(f"{prefix}:ProcessOffFV:Status3", 0)
    epics.caput(f"{prefix}:ProcessOffFV:Status4", 0)
    epics.caput(f"{prefix}:ProcessOffFV:Status5", 0)
    epics.caput(f"{prefix}:ProcessOffFV:Status6", 0)
    # clear all status PVs
    epics.caput(f"{prefix}:ProcessOn:Status1", 0)
    epics.caput(f"{prefix}:ProcessOn:Status2", 0)
    epics.caput(f"{prefix}:ProcessOn:Status3", 0)
    epics.caput(f"{prefix}:ProcessOn:Status4", 0)
    epics.caput(f"{prefix}:ProcessOn:Status5", 0)


def _stage_1(prefix: str):
    PRE_VACUUM_VALVE_SW = f"{prefix}:BBB:Relay1-SW"

    # close pre-vacuum valve (and keeps gate valve open)
    epics.caput(PRE_VACUUM_VALVE_SW, 0)

    # update UI checkbox status
    # epics.caput(PRE_VACUUM_VALVE_UI, 0)

    # wait until valve receives command to open
    while epics.caget(PRE_VACUUM_VALVE_SW):
        pass
    epics.caput(f"{prefix}:ProcessOffFV:Status1", 1)


def _stage_2(prefix: str):
    # change venting valve to manual control
    epics.caput(f"{prefix}:TURBOVAC:AK-SP", 0)
    epics.caput(f"{prefix}:TURBOVAC:PNU-SP", 134)
    epics.caput(f"{prefix}:TURBOVAC:IND-SP", 2)
    epics.caput(f"{prefix}:TURBOVAC:PWE-SP", 18)
    epics.caput(f"{prefix}:TURBOVAC:AK-SP", 7)

    # turn TURBOVAC and ACP15 pumps OFF
    epics.caput(f"{prefix}:TURBOVAC:PZD1-SP.ZRVL", 0)
    epics.caput(f"{prefix}:ACP:OnOff", 0)
    # wait until pump receives command to turn off
    while epics.caget(f"{prefix}:ACP:OnOff"):
        pass
    epics.caput(f"{prefix}:ProcessOffFV:Status2", 1)


def _stage_3(prefix: str):
    # wait until TURBOVAC frequency decrease to 600 Hz
    while epics.caget(f"{prefix}:TURBOVAC:PZD2-RB") > epics.caget(
        f"{prefix}:SYSTEM:OffFrequency"
    ):
        pass
    epics.caput(f"{prefix}:ProcessOffFV:Status3", 1)


def _stage_4(prefix: str):
    # open X203 valve (TURBOVAC venting valve)
    epics.caput(f"{prefix}:TURBOVAC:VentingValve-SW", 1)
    # update UI checkbox status
    epics.caput(f"{prefix}:TURBOVAC:VentingValve-UI", 1)
    # wait until venting valve receives command to close
    while epics.caget(f"{prefix}:TURBOVAC:VentingValve-SW") == 0:
        pass
    epics.caput(f"{prefix}:ProcessOffFV:Status4", 1)


def _stage_5(prefix: str):
    # wait until pressure gets 760 Torr
    while epics.caget(f"{prefix}:BBB:Torr") < (
        epics.caget(f"{prefix}:SYSTEM:OffPressureBase")
        * 10 ** epics.caget(f"{prefix}:SYSTEM:OffPressureExp")
    ):
        pass
    epics.caput(f"{prefix}:ProcessOffFV:Status5", 1)


def _stage_6(prefix: str):
    # valve names definition
    GATE_VALVE_SW = f"{prefix}:BBB:Relay2-SW"
    GATE_VALVE_UI = f"{prefix}:BBB:Relay2-UI"
    # Stage 6:
    # ==============================================================================
    # close all the valves (gate valve is already closed)
    epics.caput(GATE_VALVE_SW, 0)
    epics.caput(f"{prefix}:TURBOVAC:VentingValve-SW", 0)  # close X203
    # update UI checkbox status
    epics.caput(GATE_VALVE_UI, 0)
    epics.caput(f"{prefix}:TURBOVAC:VentingValve-UI", 0)  # close X203
    # wait until venting valve receives command to close
    while epics.caget(GATE_VALVE_SW):
        pass
    epics.caput(f"{prefix}:ProcessOffFV:Status6", 1)
    # ==============================================================================
    # complement value of PV to launch "Process Finished" window
    # epics.caput(VBC + ":Process:Bool", not(epics.caget(VBC + ":Process:Bool")))
    epics.caput(f"{prefix}:ProcessOff:Bool", 1)
    epics.caput(f"{prefix}:ProcessOff:Bool", 0)
    # ==============================================================================


def process_off(prefix: str):
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

    _clear_pvs(prefix=prefix)
    _stage_1(prefix=prefix)
    _stage_2(prefix=prefix)
    _stage_3(prefix=prefix)
    _stage_4(prefix=prefix)
    _stage_5(prefix=prefix)
    _stage_6(prefix=prefix)
