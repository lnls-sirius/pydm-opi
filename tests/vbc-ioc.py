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
    PVs = {
        f"{prefix}:ACP:OnOff": {"type": "float"},
        f"{prefix}:ACP:SpeedRPM": {"type": "float"},
        f"{prefix}:BBB:Relay1-SW": {"type": "float"},
        f"{prefix}:BBB:Relay1-UI.RVAL": {"type": "int"},
        f"{prefix}:BBB:Relay2-SW": {"type": "float"},
        f"{prefix}:BBB:Relay2-UI": {"type": "int"},
        f"{prefix}:BBB:Relay2-UI.RVAL": {"type": "int"},
        f"{prefix}:BBB:Relay3-UI": {"type": "int"},
        f"{prefix}:BBB:Relay3-UI.RVAL": {"type": "int"},
        f"{prefix}:BBB:Relay4-UI": {"type": "int"},
        f"{prefix}:BBB:Relay4-UI.RVAL": {"type": "int"},
        f"{prefix}:BBB:Relay5-UI": {"type": "int"},
        f"{prefix}:BBB:Relay5-UI.RVAL": {"type": "int"},
        f"{prefix}:BBB:Torr": {"type": "float"},
        f"{prefix}:BBB:TorrBase": {"type": "float"},
        f"{prefix}:BBB:TorrBaseMsg": {"type": "float"},
        f"{prefix}:BBB:TorrExpMsg": {"type": "int"},
        f"{prefix}:BBB:ValveClosed": {"type": "float"},
        f"{prefix}:BBB:ValveOpen": {"type": "float"},
        f"{prefix}:BBB:mbarBase": {"type": "string"},
        f"{prefix}:Process:TriggerOn": {"type": "int"},
        f"{prefix}:Process:TriggerPressurized": {"type": "int"},
        f"{prefix}:ProcessOff:Bool": {"type": "float"},
        f"{prefix}:ProcessOff:Bool": {"type": "int"},
        f"{prefix}:ProcessOffFV:Status1": {"type": "int"},
        f"{prefix}:ProcessOffFV:Status2": {"type": "int"},
        f"{prefix}:ProcessOffFV:Status3": {"type": "int"},
        f"{prefix}:ProcessOffFV:Status4": {"type": "int"},
        f"{prefix}:ProcessOffFV:Status5": {"type": "int"},
        f"{prefix}:ProcessOffFV:Status6": {"type": "int"},
        f"{prefix}:ProcessOn:Bool": {"type": "int"},
        f"{prefix}:ProcessOn:Status1": {"type": "int"},
        f"{prefix}:ProcessOn:Status2": {"type": "int"},
        f"{prefix}:ProcessOn:Status3": {"type": "int"},
        f"{prefix}:ProcessOn:Status4": {"type": "int"},
        f"{prefix}:ProcessOn:Status5": {"type": "int"},
        f"{prefix}:ProcessRec:Bool": {"type": "int"},
        f"{prefix}:ProcessRecovery:Status1": {"type": "int"},
        f"{prefix}:ProcessRecovery:Status2": {"type": "int"},
        f"{prefix}:ProcessRecovery:Status3": {"type": "int"},
        f"{prefix}:ProcessRecovery:Status4": {"type": "int"},
        f"{prefix}:ProcessRecovery:Status5": {"type": "int"},
        f"{prefix}:SYSTEM:Location": {"type": "str", "value": "test-ioc"},
        f"{prefix}:SYSTEM:OffFrequency": {"type": "float"},
        f"{prefix}:SYSTEM:OffPressureBase": {"type": "float"},
        f"{prefix}:SYSTEM:OffPressureExp": {"type": "float"},
        f"{prefix}:SYSTEM:OnPressureBase": {"type": "float"},
        f"{prefix}:SYSTEM:OnPressureExp": {"type": "float"},
        f"{prefix}:TURBOVAC:AK-SP": {"type": "float"},
        f"{prefix}:TURBOVAC:IND-SP": {"type": "float"},
        f"{prefix}:TURBOVAC:PNU-SP": {"type": "float"},
        f"{prefix}:TURBOVAC:PWE-SP": {"type": "float"},
        f"{prefix}:TURBOVAC:PZD1-SP.SXVL": {"type": "float"},
        f"{prefix}:TURBOVAC:PZD1-SP.TEVL": {"type": "float"},
        f"{prefix}:TURBOVAC:PZD1-SP.ZRVL": {"type": "float"},
        f"{prefix}:TURBOVAC:PZD2-RB": {"type": "float"},
        f"{prefix}:TURBOVAC:PZD2-SP": {"type": "float"},
        f"{prefix}:TURBOVAC:VentingValve-SW": {"type": "float"},
        f"{prefix}:TURBOVAC:VentingValve-UI": {"type": "int"},
        f"{prefix}:TURBOVAC:VentingValve-UI.RVAL": {"type": "float"},
    }

    # start EPICS server
    CAserver = pcaspy.SimpleServer()
    CAserver.createPV("", PVs)

    for k in PVs.keys():
        print(k)

    PSDriver()
    logger.info("IOC Started")
    while True:
        CAserver.process(0.1)


if __name__ == "__main__":
    main()
