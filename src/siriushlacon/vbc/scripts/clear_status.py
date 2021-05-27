import logging

from siriushlacon.vbc.epics import ProcessOff, ProcessOn, ProcessRecovery

logger = logging.getLogger(__name__)


def clear_status_on(prefix: str):
    """
    - clear all status PVs for 'Off Process'
    - clear all status PVs for 'Recovery Process'
    """
    logger.info("clear_status_on")

    process_off = ProcessOff(prefix=prefix)
    process_recovery = ProcessRecovery(prefix=prefix)

    process_off.clear_all_fv_status()
    process_recovery.set_all_clear()


def clear_status_off(prefix: str):
    """
    - clear all status PVs for 'On Process'
    - clear all status PVs for 'Recovery Process'
    """
    logger.info("clear_status_off")
    process_on = ProcessOn(prefix=prefix)
    process_recovery = ProcessRecovery(prefix=prefix)

    process_on.clear_all_status()
    process_recovery.set_all_clear()


def clear_status_rec(prefix: str):
    """
    - clear all status PVs for 'recovering from pressurized system' process (5*10^-2 ~ 1*10^-8)
    - clear all status PVs for 'Off Process'
    """
    process_on = ProcessOn(prefix=prefix)
    process_off = ProcessOff(prefix=prefix)

    process_on.activate_all_status()
    process_off.clear_all_fv_status()
