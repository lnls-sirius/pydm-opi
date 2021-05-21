import epics


def create_connected_pv(
    pvname: str,
    callback=None,
    form="time",
    verbose=False,
    auto_monitor=None,
    count=None,
    connection_callback=None,
    connection_timeout=None,
    access_callback=None,
) -> epics.PV:
    """Create a connected PV or raise an exception"""
    if not pvname:
        raise ValueError("pvname is empty")

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
    if not pv.connect():
        raise RuntimeError(f"PV={pv} is not connected")
    return pv
