#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydm import Display
from pydm.widgets import PyDMEmbeddedDisplay

from consts import  COLD_CATHODE, PIRANI, CC_UI, PR_UI, CC_UI, PR_UI, SETTINGS_UI
from utils import get_abs_path
from macros import *
                    
from os import path
import json

class Settings(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(Settings, self).__init__(parent=parent, args=args, macros=macros)
    
        if macros:
            if macros.get('A') == COLD_CATHODE:
                self.pdispA.macros = json.dumps(get_macro_cc(macros.get('DEVICE'), 'A'))
                self.pdispA.filename = get_abs_path(CC_UI)
            elif macros.get('A') == PIRANI:
                self.pdispA.macros = json.dumps(get_macro_pr(macros.get('DEVICE'), 'A'))
                self.pdispA.filename = get_abs_path(PR_UI)
        
            if macros.get('B') == COLD_CATHODE:
                self.pdispB.macros = json.dumps(get_macro_cc(macros.get('DEVICE'), 'B'))
                self.pdispB.filename = get_abs_path(CC_UI)
            elif macros.get('B') == PIRANI:
                self.pdispB.macros = json.dumps(get_macro_pr(macros.get('DEVICE'), 'B'))
                self.pdispB.filename =  get_abs_path(PR_UI)
        
            if macros.get('C') == COLD_CATHODE:
                self.pdispC.macros = json.dumps(get_macro_cc(macros.get('DEVICE'), 'C'))
                self.pdispC.filename = get_abs_path(CC_UI)
            elif macros.get('C') == PIRANI:
                self.pdispC.macros = json.dumps(get_macro_pr(macros.get('DEVICE'), 'C'))
                self.pdispC.filename =  get_abs_path(PR_UI)

        self.pdispA.setAutoFillBackground(False)
        self.pdispB.setAutoFillBackground(False)
        self.pdispC.setAutoFillBackground(False)

    def ui_filename(self):
        return SETTINGS_UI

    def ui_filepath(self):
        return get_abs_path(SETTINGS_UI)