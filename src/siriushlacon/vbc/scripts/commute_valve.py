import logging
import time

from siriushlacon.utils.epics import create_connected_pv

logger = logging.getLogger(__name__)


def _venting_valve(prefix: str, confirmed: bool):
    """
    this is script is used to commute a valve value
    """
    logger.info("venting_valve")
    turbovac_venting_valve_pv = create_connected_pv(
        pvname=f"{prefix}:TURBOVAC:VentingValve-SW"
    )
    turbovac_venting_valve_ui_pv = create_connected_pv(
        pvname=f"{prefix}:TURBOVAC:VentingValve-UI.RVAL"
    )

    time.sleep(1)  # why?!

    # if relay swtiching message is confirmed, change PV SW values:
    if confirmed:
        turbovac_venting_valve_pv.value = not (turbovac_venting_valve_pv.value)

    # if relay swtiching message is canceled, do nothing:
    else:
        turbovac_venting_valve_ui_pv.value = turbovac_venting_valve_pv.value


def _relay(prefix: str, valve: int, confirmed: bool):
    """
    this is script is used to commute a valve value
    """
    logger.info("relay")

    sw_pv = create_connected_pv(pvname=f"{prefix}:BBB:Relay{valve}-SW")
    ui_pv = create_connected_pv(pvname=f"{prefix}:BBB:Relay{valve}-UI.RVAL")

    time.sleep(1)  # why?!

    # if relay swtiching message is confirmed, change PV SW values:
    if confirmed:
        sw_pv.value = not (sw_pv.value)

    # if relay swtiching message is canceled, do nothing:
    else:
        ui_pv.value = sw_pv.value


def commute_valve(prefix: str, valve: int, confirmed: bool):
    """
    this is script is used to commute a valve value
    """

    if valve >= 1 and valve <= 4:
        _relay(prefix=prefix, valve=valve, confirmed=confirmed)
    elif valve == 5:
        _venting_valve(prefix=prefix, confirmed=confirmed)
    else:
        raise ValueError(f"Invalid valve value '{valve}'")
