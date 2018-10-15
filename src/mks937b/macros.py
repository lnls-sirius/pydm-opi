#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from consts import COLD_CATHODE, PIRANI
# @todo: DO BETTER !


def get_device_macro(device, a, b, c):
    return {
        "DEVICE": device,
        "A": a,
        "B": b,
        "C": c
    }


def get_macro_cc(device, gauge):
    if gauge == 'A':
        return{
            "DEVICE": device,
            "r1": "1", "r2": "2", "r3": "3", "r4": "4",
            "GAUGE": "A1", "channel": "1"
        }
    if gauge == 'B':
        return{
            "DEVICE": device,
            "r1": "5", "r2": "6", "r3": "7", "r4": "8",
            "GAUGE": "B1", "channel": "3"
        }
    if gauge == 'C':
        return{
            "DEVICE": device,
            "r1": "9", "r2": "10", "r3": "11", "r4": "12",
            "GAUGE": "C1", "channel": "5"
        }
    return {
        "DEVICE": "",
        "r1": "", "r2": "", "r3": "", "r4": "",
        "GAUGE": "", "channel": ""
    }


def get_macro_pr(device, gauge):
    if gauge == 'A':
        return{
            "DEVICE": device,
            "r1": "1", "r2": "2", "r3": "3", "r4": "4",
            "GAUGE_1": "A1", "GAUGE_2": "A2", "channel_1": "1", "channel_2": "2"
        }
    elif gauge == 'B':
        return{
            "DEVICE": device,
            "r1": "5", "r2": "6", "r3": "7", "r4": "8",
            "GAUGE_1": "B1", "GAUGE_2": "B2", "channel_1": "3", "channel_2": "4"
        }
    elif gauge == 'C':
        return{
            "DEVICE": device,
            "r1": "9", "r2": "10", "r3": "11", "r4": "12",
            "GAUGE_1": "C1", "GAUGE_2": "C2", "channel_1": "5", "channel_2": "6"
        }

    return {
        "DEVICE": "",
        "r1": "", "r2": "", "r3": "", "r4": "",
        "GAUGE": "", "channel_1": "", "channel_2": ""
    }
