import epics
import time


def commute_valve(prefix: str, valve: int, confirmed: bool):
    """
    this is script is used to commute a valve value
    """
    sw_pv = epics.PV(pvname=f"{prefix}:BBB:Relay{valve}-SW")
    ui_pv = epics.PV(pvname=f"{prefix}:BBB:Relay{valve}-UI.RVAL")
    turbovac_venting_valve_pv = epics.PV(pvname=f"{prefix}:TURBOVAC:VentingValve-SW")
    turbovac_venting_valve_ui_pv = epics.PV(
        pvname=f"{prefix}:TURBOVAC:VentingValve-UI.RVAL"
    )

    time.sleep(1)

    # if relay swtiching message is confirmed, change PV SW values:
    if confirmed:
        if valve >= 1 and valve <= 4:
            sw_pv.value = not (sw_pv.value)
        elif valve == 5:
            turbovac_venting_valve_pv.value = not (turbovac_venting_valve_pv.value)

    # if relay swtiching message is canceled, do nothing:
    else:
        if valve >= 1 and valve <= 4:
            ui_pv.value = sw_pv.value
        elif valve == 5:
            turbovac_venting_valve_ui_pv.value = turbovac_venting_valve_pv.value
