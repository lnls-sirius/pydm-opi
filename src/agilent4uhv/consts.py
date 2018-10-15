#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform

ring_sub_sectors = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
ring_sector_devices = [
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['D3EVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
 
    ['DEV2ICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEV1ICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
 
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
 
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
 
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
 
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
 
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
 
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
 
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
 
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4']
]

booster_sub_sectors = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
booster_sector_devices = [
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
        
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
        
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
        
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
        
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
        
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
        
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
        
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
        
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
        
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4']
]

ltb_sub_sectors = ['1']
ltb_sector_devices = [
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4']
]

bts_sub_sectors = ['1']
bts_sector_devices = [
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4'],
    ['DEVICE', 'CH1', 'CH2', 'CH3', 'CH4']
]