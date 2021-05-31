import time

import epics


def create_connected_pv(
    pvname: str,
    callback=None,
    form="time",
    verbose=False,
    auto_monitor=None,
    count=None,
    connection_callback=None,
    connection_timeout=5.0,
    access_callback=None,
    attempt_max: int = 2,
    attempt_delay: float = 0.5,
) -> epics.PV:
    """Create a connected PV or raise an exception"""
    if not pvname:
        raise ValueError("pvname is empty")

    if attempt_delay <= 0:
        attempt_delay = 0.05

    _attempt = 0
    pv = epics.PV(
        pvname=pvname,
        callback=callback,
        form=form,
        verbose=verbose,
        auto_monitor=auto_monitor,
        count=count,
        connection_callback=connection_callback,
        connection_timeout=connection_timeout,
        access_callback=access_callback,
    )

    while _attempt < attempt_max:
        if pv.connect():
            break
        time.sleep(attempt_delay)
        _attempt += 1

    if not pv.connect():
        raise RuntimeError(f"PV={pv} is not connected")
    return pv
