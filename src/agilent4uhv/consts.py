#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform

ring_sub_sectors = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
ring_sector_devices = [
    ['DEVICE1', 'D1:CH1', 'D1:CH2', 'D1:CH3', 'D1:CH4'],
    ['DEVICE2', 'D2:CH1', 'D2:CH2', 'D2:CH3', 'D2:CH4'],
    ['DEVICE3', 'D3:CH1', 'D3:CH2', 'D3:CH3', 'D3:CH4'],
    ['DEVICE4', 'D4:CH1', 'D4:CH2', 'D4:CH3', 'D4:CH4'],
 
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
    ['asd', 'CH1', 'CH2', 'CH3', 'CH4']
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