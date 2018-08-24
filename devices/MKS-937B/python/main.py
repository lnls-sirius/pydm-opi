#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydm import Display
from os import path

from utils import get_abs_path
from consts import MAIN_UI, STORAGE_RING_PY, BOOSTER_PY, BTS_PY, LTB_PY
from pydm.utilities import IconFont

class Main(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(Main, self).__init__(parent=parent, args=args, macros=macros)
        
        self.btnRing.displayFilename = get_abs_path(get_abs_path(STORAGE_RING_PY)) 
        self.btnRing.setIcon(IconFont().icon('circle'))
        
        self.btnBooster.displayFilename = get_abs_path(get_abs_path(BOOSTER_PY)) 
        self.btnBooster.setIcon(IconFont().icon('forward'))
                
        self.btnBts.displayFilename = get_abs_path(get_abs_path(BTS_PY)) 
        self.btnBts.setIcon(IconFont().icon('arrow-right'))

        self.btnLtb.displayFilename = get_abs_path(get_abs_path(LTB_PY)) 
        self.btnLtb.setIcon(IconFont().icon('arrow-right'))

    def ui_filename(self):
        return MAIN_UI

    def ui_filepath(self):
        return get_abs_path(MAIN_UI)