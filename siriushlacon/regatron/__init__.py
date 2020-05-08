#!/usr/local/env python3
import logging
import threading

import epics

from siriushlacon.regatron.consts import STD_READINGS, EXT_READINGS

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


def proc_alarm(mod=True, std=False, timeout=1.0, error=True, prefix=None):
    """
    Start a worker that will PROC every PV in the selected category.

    :param mod: Regatron's module or system group
    :param std: Standard or extended errors/warnings
    :param timeout: Caput timeout
    :param error: Error or warning group
    :param prefix: PV prefix
    """
    if not prefix:
        raise Exception("prefix not defined")

    _lock = lock(error, std)
    if not _lock["working"]:
        with _lock["lock"]:
            _lock["working"] = True
            _1 = prefix
            _2 = "Mod" if mod else "Sys"
            _3 = "Std" if std else "Ext"
            _4 = "Err" if error else "Warn"
            pvs = []

            readings = STD_READINGS if std else EXT_READINGS
            for r in readings:
                pv = "{}:{}:{}{}{}.PROC".format(_1, _2, _3, _4, r)
                pvs.append(pv)
            worker = threading.Thread(
                target=do_work,
                daemon=True,
                kwargs={"pvs": pvs, "timeout": timeout, "_lock": _lock},
            )
            worker.start()


def do_work(pvs, timeout, _lock):
    """ Worker function """
    logger.info("Thread doing work ...")
    with _lock["lock"]:
        for pv in pvs:
            epics.caput(pv, 1, timeout=timeout)
            logger.info("Caput {}".format(pv))
        _lock["working"] = False

    logger.info("Work done.")
