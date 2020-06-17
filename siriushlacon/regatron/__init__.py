#!/usr/local/env python3
import logging
import threading

import epics

from siriushlacon.regatron.consts import READINGS

logger = logging.getLogger()

std_err_lock = {"lock": threading.RLock(), "working": False}
std_warn_lock = {"lock": threading.RLock(), "working": False}

ext_err_lock = {"lock": threading.RLock(), "working": False}
ext_warn_lock = {"lock": threading.RLock(), "working": False}


def lock(error, std):
    if error:
        return std_err_lock if std else ext_err_lock
    else:
        return std_warn_lock if std else ext_warn_lock


def do_work(pvs, timeout, _lock):
    """ Worker function """
    logger.info("Thread doing work ...")
    with _lock["lock"]:
        for pv in pvs:
            epics.caput(pv, 1, timeout=timeout)
            logger.info("Caput {}".format(pv))
        _lock["working"] = False

    logger.info("Work done.")
