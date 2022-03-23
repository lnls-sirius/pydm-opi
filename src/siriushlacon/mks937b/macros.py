#!/usr/bin/env python3


def get_device_macro(device, a, b, c, **kwargs):
    return {
        "DEVICE": device,
        "A": a,
        "B": b,
        "C": c,
        "G1": kwargs["G1"],
        "G2": kwargs["G2"],
        "G3": kwargs["G3"],
        "G4": kwargs["G4"],
        "G5": kwargs["G5"],
        "G6": kwargs["G6"],
    }


def get_macro(device, gauge, *args):
    macro = {
        "DEVICE": device,
        "r1": "",
        "r2": "",
        "r3": "",
        "r4": "",
        "GAUGE": gauge,
        "channel": "",
        "GA": "",
        "GB": "",
    }

    macro["GA"] = args[0]
    macro["GB"] = args[1]

    if gauge == "A":
        macro["r1"] = "1"
        macro["r2"] = "2"
        macro["r3"] = "3"
        macro["r4"] = "4"
        macro["channel"] = "1"

    elif gauge == "B":
        macro["r1"] = "5"
        macro["r2"] = "6"
        macro["r3"] = "7"
        macro["r4"] = "8"
        macro["channel"] = "3"

    elif gauge == "C":
        macro["r1"] = "9"
        macro["r2"] = "10"
        macro["r3"] = "11"
        macro["r4"] = "12"
        macro["channel"] = "5"

    return macro
