#!/usr/bin/env python3
import conscommon.data as data
import conscommon.data_model as data_model

data = data_model.getDevicesFromBeagles(data_model.getBeaglesFromList(data.getMKS()))

rows = []
with open("hist.txt", "r") as _f:
    rows = _f.readlines()

for row in rows:
    _d = row.split(" ")[6:]
    pv = _d[4]

    for device in data:
        if device.prefix in pv:
            if "Relay1" in pv:
                print(
                    "[{} {}] {:25s} {} {:15s} {:15s}  {:15s} {:15s}".format(
                        *_d[0:2], device.channels[2].prefix, *_d[4:], *_d[2:4]
                    ).replace("\n", "")
                )
            if "Relay5" in pv or "Relay7" in pv:
                print(
                    "[{} {}] {:25s} {} {:15s} {:15s}  {:15s} {:15s}".format(
                        *_d[0:2], device.channels[2].prefix, *_d[4:], *_d[2:4]
                    ).replace("\n", "")
                )
