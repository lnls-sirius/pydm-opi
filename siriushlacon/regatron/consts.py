#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pkg_resources
import json


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


DATA_JSON = get_abs_path("data.json")
REGATRON_MAIN = get_abs_path("main.py")
TREE_32 = get_abs_path("tree.py")
COMPLETE_MAIN = get_abs_path("regatron.py")
ALARM_MAIN = get_abs_path("alarm.py")

REGATRON_UI = get_abs_path("ui/main.ui")
TREE_32_UI = get_abs_path("ui/tree32.ui")
COMPLETE_UI = get_abs_path("ui/regatron.ui")
ALARM_UI = get_abs_path("ui/alarm.ui")


def load_data():
    data = None
    with open(DATA_JSON, "r") as f:
        data = json.load(f)
    return data


REGATRON_DEVICES = {}
for d in load_data():
    REGATRON_DEVICES[d["P"]] = {**d}

ERROR_LIST_PDF = get_abs_path("ui/error-list-en.pdf")
CODES = [
    *[str(i) for i in range(10)],
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "J",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
]
READINGS_MAP = {
    # STANDARD_MAP
    0: "Internal",
    1: "Internal (PDSP)",
    2: "Output Current",
    3: "Output Voltage",
    4: "Supply",
    5: "Temperature",
    6: "Communication",
    7: "Internal (Modulator)",
    8: "Internal (AD overrange 1)",
    9: "Internal (AD overrange 2)",
    10: "Internal (AD underrange 1)",
    11: "Internal (AD underrange 2)",
    12: "Login",
    13: "Configuration",
    14: "Configuration 2",
    15: "Miscellaneous",
    # EXTENDED_MAP = {
    16: "IBC System",
    17: "IBC Supply",
    18: "IBC Communication",
    19: "IBC Power",
    20: "IBC Inverter",
    21: "IBC Miscellaneous",
    22: "IBC Inverter 2",
    23: "not used",
    24: "Configuration 4",
    25: "Miscellaneous 2",
    26: "Supply 2",
    27: "Login 2",
    28: "Configuration 3",
    29: "Communication 3",
    30: "Internal 2",
    31: "Communication 2",
}

# READINGS = [
STD_READINGS = [
    "Intrn-Mon",
    "IntrnPDSP-Mon",
    "OutCurrent-Mon",
    "OutVolt-Mon",
    "Supply-Mon",
    "T-Mon",
    "Comm-Mon",
    "IntrnMod-Mon",
    "AD1Ovr-Mon",
    "AD2Ovr-Mon",
    "AD1Undr-Mon",
    "AD2Undr-Mon",
    "Login-Mon",
    "Conf-Mon",
    "Conf2-Mon",
    "Misc-Mon",
]
EXT_READINGS = [
    "IBCSystem-Mon",
    "IBCSuppply-Mon",
    "IBCComm-Mon",
    "IBCPwr-Mon1",
    "IBCInv-Mon",
    "IBCMisc-Mon",
    "IBCInv2-Mon",
    "P-Mon",
    "Conf4-Mon",
    "Misc2-Mon",
    "Supply2-Mon",
    "Login2-Mon",
    "Conf3-Mon",
    "Comm3-Mon",
    "Intrn2-Mon",
    "Comm2-Mon",
]
