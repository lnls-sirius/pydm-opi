#!/usr/bin/env python3
import epics

from conscommon.data import getMKS
from conscommon.data_model import getBeaglesFromList, getDevicesFromBeagles


def set_mks_channel_on():
    for device in getDevicesFromBeagles(getBeaglesFromList(getMKS())):
        if not device.enable:
            continue
        for channel in device.channels:
            if not channel.enable:
                continue
        epics.caput(channel.prefix + ":Enable-SP", 1)


if __name__ == "__main__":
    set_mks_channel_on()
