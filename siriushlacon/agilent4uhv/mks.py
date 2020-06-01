#!/usr/bin/env python3
import conscommon.data as data
import conscommon.data_model as data_model

if __name__ == "__main__":
    for device in data_model.getDevicesFromBeagles(
        data_model.getBeaglesFromList(data.getMKS())
    ):
        if "BAK" in device.prefix:
            continue

        for _n in [1, 5]:
            n = str(_n)
            print(device.prefix + ":Relay" + n + ":Hyst-SP")
            print(device.prefix + ":Relay" + n + ":Hyst-RB")
            # print(device.prefix + ":Relay" + n + ":Setpoint-SP")
            # print(device.prefix + ":Relay" + n + ":Setpoint-RB")
            # print(device.prefix + ":Relay" + n + ":SetpointStatus-Mon")
