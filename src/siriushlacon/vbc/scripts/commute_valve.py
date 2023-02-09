import logging
import time

from siriushlacon.epics import create_connected_pv

_logger = logging.getLogger(__name__)


def set_venting_valve_state(prefix: str, state: bool):
    """Set venting valve state :param state: On=True, Off=False"""
    _logger.info(f"set turbo venting valve state {state}")
    turbovac_venting_valve_pv = create_connected_pv(
        pvname=f"{prefix}:TURBOVAC:VentingValve-SW"
    )

    turbovac_venting_valve_pv.value = 1 if state else 0


def _commute_venting_valve(prefix: str, confirmed: bool):
    """
    this is script is used to commute a valve value
    """
    _logger.info(f"{prefix} confirmed={confirmed}")
    turbovac_venting_valve_pv = create_connected_pv(
        pvname=f"{prefix}:TURBOVAC:VentingValve-SW"
    )
    turbovac_venting_valve_ui_pv = create_connected_pv(
        pvname=f"{prefix}:TURBOVAC:VentingValve-UI.RVAL"
    )

    time.sleep(1)  # why?!
    _logger.info(f"pv sw update {prefix} confirmed={confirmed}")

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
    _logger.info("relay  prefix={prefix} valve={valve} confirmed={confirmed}")

    sw_pv = create_connected_pv(pvname=f"{prefix}:BBB:Relay{valve}-SW")
    ui_pv = create_connected_pv(pvname=f"{prefix}:BBB:Relay{valve}-UI.RVAL")

    time.sleep(1)  # why?!

    _logger.info(f"pv sw update prefix={prefix} valve={valve} confirmed={confirmed}")
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
    _logger.info(f"prefix={prefix} value={valve} confirmed={confirmed}")
    if valve >= 1 and valve <= 4:
        _relay(prefix=prefix, valve=valve, confirmed=confirmed)
    elif valve == 5:
        _commute_venting_valve(prefix=prefix, confirmed=confirmed)
    else:
        raise ValueError(f"Invalid valve value {valve!r}")
