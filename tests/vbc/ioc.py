#!/usr/bin/env python3
import argparse

import pcaspy
from log import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="VBC Dummy IOC")
    parser.add_argument(
        "--prefix",
        type=str,
        default="VBC1",
        help="IOC prefix",
        required=False,
        dest="prefix",
    )
    args = parser.parse_args()

    ioc(prefix=args.prefix)


class PSDriver(pcaspy.Driver):
    # class constructor
    def __init__(self):
        # call the superclass constructor
        pcaspy.Driver.__init__(self)

    # writing in PVs function
    def write(self, reason, value):
        self.setParam(reason, value)
        self.updatePVs()
        logger.info(f"Write at '{reason}': {value}")
        return True


def ioc(prefix: str):
    PVs = {}
    # -----------------------------------------------
    # status PVs for "turning the system ON" process
    PVs[f"{prefix}:ProcessOn:Status1"] = {"type": "int"}
    PVs[f"{prefix}:ProcessOn:Status2"] = {"type": "int"}
    PVs[f"{prefix}:ProcessOn:Status3"] = {"type": "int"}
    PVs[f"{prefix}:ProcessOn:Status4"] = {"type": "int"}
    PVs[f"{prefix}:ProcessOn:Status5"] = {"type": "int"}
    # -----------------------------------------------
    # status PVs for "turning the system OFF" process (FV = full ventilation)
    PVs[f"{prefix}:ProcessOffFV:Status1"] = {"type": "int"}
    PVs[f"{prefix}:ProcessOffFV:Status2"] = {"type": "int"}
    PVs[f"{prefix}:ProcessOffFV:Status3"] = {"type": "int"}
    PVs[f"{prefix}:ProcessOffFV:Status4"] = {"type": "int"}
    PVs[f"{prefix}:ProcessOffFV:Status5"] = {"type": "int"}
    PVs[f"{prefix}:ProcessOffFV:Status6"] = {"type": "int"}
    # -----------------------------------------------
    # status PVs for "turning the system OFF" process (NV = no ventilation)
    # PVs["VBC" + VBC + ":ProcessOffNV:Status1"] = {"type" : "int"}
    # PVs["VBC" + VBC + ":ProcessOffNV:Status2"] = {"type" : "int"}
    # PVs["VBC" + VBC + ":ProcessOffNV:Status3"] = {"type" : "int"}
    # PVs["VBC" + VBC + ":ProcessOffNV:Status4"] = {"type" : "int"}
    # PVs["VBC" + VBC + ":ProcessOffNV:Status5"] = {"type" : "int"}
    # PVs["VBC" + VBC + ":ProcessOffNV:Status6"] = {"type" : "int"}
    # -----------------------------------------------
    # status PVs for "recovering from pressurized system" process (5*10^-2 ~ 1*10^-8)
    PVs[f"{prefix}:ProcessRecovery:Status1"] = {"type": "int"}
    PVs[f"{prefix}:ProcessRecovery:Status2"] = {"type": "int"}
    PVs[f"{prefix}:ProcessRecovery:Status3"] = {"type": "int"}
    PVs[f"{prefix}:ProcessRecovery:Status4"] = {"type": "int"}
    PVs[f"{prefix}:ProcessRecovery:Status5"] = {"type": "int"}
    # -----------------------------------------------
    PVs[f"{prefix}:ProcessOn:Bool"] = {"type": "int"}
    PVs[f"{prefix}:ProcessOff:Bool"] = {"type": "int"}
    PVs[f"{prefix}:ProcessRec:Bool"] = {"type": "int"}
    PVs[f"{prefix}:Process:TriggerOn"] = {"type": "int"}
    PVs[f"{prefix}:Process:TriggerPressurized"] = {"type": "int"}

    # start EPICS server
    CAserver = pcaspy.SimpleServer()
    CAserver.createPV("", PVs)

    PSDriver()
    logger.info("IOC Started")
    while True:
        CAserver.process(0.1)


if __name__ == "__main__":
    main()
