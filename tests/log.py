import logging
from typing import Dict

loggers: Dict[str, logging.Logger] = {}


def get_logger(name):
    logger = logging.getLogger(name)

    if name not in loggers:
        loggers[name if name else "root"] = logger

    if name:
        return logger

    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(name)s [%(filename)s:%(lineno)s %(funcName)s] - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


logger = get_logger(None)


def set_level_global(level):
    global loggers

    for _, l in loggers.items():
        l.setLevel(level)
