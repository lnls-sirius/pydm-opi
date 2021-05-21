from siriushlacon.utils.epics import create_connected_pv


def _enable_on_process(prefix: str):
    """clear all status PVs for 'recovering from pressurized system' process (5*10^-2 ~ 1*10^-8)"""
    on_status1_pv = create_connected_pv(pvname=f"{prefix}:ProcessOn:Status1")
    on_status2_pv = create_connected_pv(pvname=f"{prefix}:ProcessOn:Status2")
    on_status3_pv = create_connected_pv(pvname=f"{prefix}:ProcessOn:Status3")
    on_status4_pv = create_connected_pv(pvname=f"{prefix}:ProcessOn:Status4")
    on_status5_pv = create_connected_pv(pvname=f"{prefix}:ProcessOn:Status5")

    on_status1_pv.value = 1
    on_status2_pv.value = 1
    on_status3_pv.value = 1
    on_status4_pv.value = 1
    on_status5_pv.value = 1


def _clear_on_process(prefix: str):
    """clear all status PVs for 'On Process'"""
    on_status1_pv = create_connected_pv(pvname=f"{prefix}:ProcessOn:Status1")
    on_status2_pv = create_connected_pv(pvname=f"{prefix}:ProcessOn:Status2")
    on_status3_pv = create_connected_pv(pvname=f"{prefix}:ProcessOn:Status3")
    on_status4_pv = create_connected_pv(pvname=f"{prefix}:ProcessOn:Status4")
    on_status5_pv = create_connected_pv(pvname=f"{prefix}:ProcessOn:Status5")

    on_status1_pv.value = 0
    on_status2_pv.value = 0
    on_status3_pv.value = 0
    on_status4_pv.value = 0
    on_status5_pv.value = 0


def _clear_off_process(prefix: str):
    """clear all status PVs for 'Off Process'"""
    off_fv_status1_pv = create_connected_pv(pvname=f"{prefix}:ProcessOffFV:Status1")
    off_fv_status2_pv = create_connected_pv(pvname=f"{prefix}:ProcessOffFV:Status2")
    off_fv_status3_pv = create_connected_pv(pvname=f"{prefix}:ProcessOffFV:Status3")
    off_fv_status4_pv = create_connected_pv(pvname=f"{prefix}:ProcessOffFV:Status4")
    off_fv_status5_pv = create_connected_pv(pvname=f"{prefix}:ProcessOffFV:Status5")
    off_fv_status6_pv = create_connected_pv(pvname=f"{prefix}:ProcessOffFV:Status6")

    off_fv_status1_pv.value = 0
    off_fv_status2_pv.value = 0
    off_fv_status3_pv.value = 0
    off_fv_status4_pv.value = 0
    off_fv_status5_pv.value = 0
    off_fv_status6_pv.value = 0


def _clear_recovery_process(prefix: str):
    """clear all status PVs for 'Recovery Process'"""
    prec_status1_pv = create_connected_pv(pvname=f"{prefix}:ProcessRecovery:Status1")
    prec_status2_pv = create_connected_pv(pvname=f"{prefix}:ProcessRecovery:Status2")
    prec_status3_pv = create_connected_pv(pvname=f"{prefix}:ProcessRecovery:Status3")
    prec_status4_pv = create_connected_pv(pvname=f"{prefix}:ProcessRecovery:Status4")
    prec_status5_pv = create_connected_pv(pvname=f"{prefix}:ProcessRecovery:Status5")

    prec_status1_pv.value = 0
    prec_status2_pv.value = 0
    prec_status3_pv.value = 0
    prec_status4_pv.value = 0
    prec_status5_pv.value = 0


def clear_status_on(prefix: str):
    _clear_off_process(prefix=prefix)
    _clear_recovery_process(prefix=prefix)


def clear_status_off(prefix: str):
    _clear_on_process(prefix=prefix)
    _clear_recovery_process(prefix=prefix)


def clear_status_rec(prefix: str):
    _enable_on_process(prefix=prefix)
    _clear_off_process(prefix=prefix)
