#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform

ring_sub_sectors = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
ring_sector_devices = [
    ['D1', 'D1:CH1', 'D1:CH2', 'D1:CH3', 'D1:CH4'],
    ['D2', 'D2:CH1', 'D2:CH2', 'D2:CH3', 'D2:CH4'],
    ['D3', 'D3:CH1', 'D3:CH2', 'D3:CH3', 'D3:CH4'],
    ['D4', 'D4:CH1', 'D4:CH2', 'D4:CH3', 'D4:CH4'],
 
    ['DEVICE:A', 'A:CH1', 'A:CH2', 'A:CH3', 'A:CH4'],
    ['DEVICE:A', 'A:CH1', 'A:CH2', 'A:CH3', 'A:CH4'],
    ['DEVICE:A', 'A:CH1', 'A:CH2', 'A:CH3', 'A:CH4'],
    ['DEVICE:A', 'A:CH1', 'A:CH2', 'A:CH3', 'A:CH4'],
 
    ['DEVICE:B', 'B:CH1', 'B:CH2', 'B:CH3', 'B:CH4'],
    ['DEVICE:B', 'B:CH1', 'B:CH2', 'B:CH3', 'B:CH4'],
    ['DEVICE:B', 'B:CH1', 'B:CH2', 'B:CH3', 'B:CH4'],
    ['DEVICE:B', 'B:CH1', 'B:CH2', 'B:CH3', 'B:CH4'],
 
    ['DEVICE:C', 'C:CH1', 'C:CH2', 'C:CH3', 'C:CH4'],
    ['DEVICE:C', 'C:CH1', 'C:CH2', 'C:CH3', 'C:CH4'],
    ['DEVICE:C', 'C:CH1', 'C:CH2', 'C:CH3', 'C:CH4'],
    ['DEVICE:C', 'C:CH1', 'C:CH2', 'C:CH3', 'C:CH4'],
 
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
 
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
 
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
 
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
 
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
 
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['DEVICE:D', 'CH1:D', 'CH2:D', 'CH3:D', 'CH4:D'],
    ['RandomName', 'CH1', 'CH2', 'CH3', 'DH4']
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