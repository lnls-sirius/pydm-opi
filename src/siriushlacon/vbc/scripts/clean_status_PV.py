import epics

from siriushlacon.vbc.consts import Finished


def clean_status_pv(prefix: str, finished: Finished):
    """
    this script clean all the status PV for both On/Off Process
    """
    # called after ON process is finished
    if finished == Finished.ON:
        # clear all status PVs for "Off Process"
        epics.caput(f"{prefix}:ProcessOffFV:Status1", 0)
        epics.caput(f"{prefix}:ProcessOffFV:Status2", 0)
        epics.caput(f"{prefix}:ProcessOffFV:Status3", 0)
        epics.caput(f"{prefix}:ProcessOffFV:Status4", 0)
        epics.caput(f"{prefix}:ProcessOffFV:Status5", 0)
        epics.caput(f"{prefix}:ProcessOffFV:Status6", 0)
        # clear all status PVs for "Recovery Process"
        epics.caput(f"{prefix}:ProcessRecovery:Status1", 0)
        epics.caput(f"{prefix}:ProcessRecovery:Status2", 0)
        epics.caput(f"{prefix}:ProcessRecovery:Status3", 0)
        epics.caput(f"{prefix}:ProcessRecovery:Status4", 0)
        epics.caput(f"{prefix}:ProcessRecovery:Status5", 0)

    # called after OFF process is finished
    elif finished == Finished.OFF:
        # clear all status PVs for "On Process"
        epics.caput(f"{prefix}:ProcessOn:Status1", 0)
        epics.caput(f"{prefix}:ProcessOn:Status2", 0)
        epics.caput(f"{prefix}:ProcessOn:Status3", 0)
        epics.caput(f"{prefix}:ProcessOn:Status4", 0)
        epics.caput(f"{prefix}:ProcessOn:Status5", 0)
        # clear all status PVs for "Recovery Process"
        epics.caput(f"{prefix}:ProcessRecovery:Status1", 0)
        epics.caput(f"{prefix}:ProcessRecovery:Status2", 0)
        epics.caput(f"{prefix}:ProcessRecovery:Status3", 0)
        epics.caput(f"{prefix}:ProcessRecovery:Status4", 0)
        epics.caput(f"{prefix}:ProcessRecovery:Status5", 0)

    # called after REC process is finished
    elif finished == Finished.REC:
        # clear all status PVs for "recovering from pressurized system" process (5*10^-2 ~ 1*10^-8)
        epics.caput(f"{prefix}:ProcessOn:Status1", 1)
        epics.caput(f"{prefix}:ProcessOn:Status2", 1)
        epics.caput(f"{prefix}:ProcessOn:Status3", 1)
        epics.caput(f"{prefix}:ProcessOn:Status4", 1)
        epics.caput(f"{prefix}:ProcessOn:Status5", 1)
        # clear all status PVs for "Off Process"
        epics.caput(f"{prefix}:ProcessOffFV:Status1", 0)
        epics.caput(f"{prefix}:ProcessOffFV:Status2", 0)
        epics.caput(f"{prefix}:ProcessOffFV:Status3", 0)
        epics.caput(f"{prefix}:ProcessOffFV:Status4", 0)
        epics.caput(f"{prefix}:ProcessOffFV:Status5", 0)
        epics.caput(f"{prefix}:ProcessOffFV:Status6", 0)
