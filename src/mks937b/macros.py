#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from consts import COLD_CATHODE, PIRANI
# @todo: DO BETTER !


def get_device_macro(device, a, b, c, **kwargs):
    return {
        "DEVICE": device,
        "A": a,
        "B": b,
        "C": c,
        "G1" : kwargs['G1'],
        "G2" : kwargs['G2'],
        "G3" : kwargs['G3'],
        "G4" : kwargs['G4'],
        "G5" : kwargs['G5'],
        "G6" : kwargs['G6']
    }


def get_macro(device, gauge, *args):
    if gauge == 'A':
        return{
            "DEVICE": device,
            "r1": "1",
            "r2": "2", 
            "r3": "3", 
            "r4": "4",
            "GAUGE": "A1", "channel": "1",
            "GA" : args[0],
            "GB" : args[1]
        }
        
    if gauge == 'B':
        return{
            "DEVICE": device,
            "r1": "5",
            "r2": "6",
            "r3": "7",
            "r4": "8",
            "GAUGE": "B1", "channel": "3",
            "GA" : args[0],
            "GB" : args[1]
        }
    if gauge == 'C':
        return{
            "DEVICE": device,
            "r1": "9",
            "r2": "10",
            "r3": "11",
            "r4": "12",
            "GAUGE": "C1", "channel": "5",
            "GA" : args[0],
            "GB" : args[1]
        }
    return {
        "DEVICE": "",
        "r1": "",
        "r2": "",
        "r3": "",
        "r4": "",
        "GAUGE": "", "channel": "",
        "GA" : "",
        "GB" : ""
    }
    