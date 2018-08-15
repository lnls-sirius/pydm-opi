#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydm import Display
from pydm.widgets import PyDMEmbeddedDisplay

from consts import  COLD_CATHODE, PIRANI
                    
from macros import *
                    
from os import path
import json
#from pydm.PyQt5.QtWidgets import QPushButton

class Settings(Display):
  def __init__(self, parent=None, args=[], macros=None):
    super(Settings, self).__init__(parent=parent, args=args, macros=macros)
 
    if macros:
        if macros.get('A') == COLD_CATHODE:
            self.pdispA.macros = json.dumps(get_macro_cc(macros.get('DEVICE'), 'A'))
            self.pdispA.filename = '../ui/cc.ui' 
        elif macros.get('A') == PIRANI:
            self.pdispA.macros = json.dumps(get_macro_pr(macros.get('DEVICE'), 'A'))
            self.pdispA.filename = '../ui/pirani.ui'
    
        if macros.get('B') == COLD_CATHODE:
            self.pdispB.macros = json.dumps(get_macro_cc(macros.get('DEVICE'), 'B'))
            self.pdispB.filename = '../ui/cc.ui' 
        elif macros.get('B') == PIRANI:
            self.pdispB.macros = json.dumps(get_macro_pr(macros.get('DEVICE'), 'B'))
            self.pdispB.filename = '../ui/pirani.ui'
    
        if macros.get('C') == COLD_CATHODE:
            self.pdispC.macros = json.dumps(get_macro_cc(macros.get('DEVICE'), 'C'))
            self.pdispC.filename = '../ui/cc.ui' 
        elif macros.get('C') == PIRANI:
            self.pdispC.macros = json.dumps(get_macro_pr(macros.get('DEVICE'), 'C'))
            self.pdispC.filename = '../ui/pirani.ui'
 

  def ui_filename(self):
    return '../ui/settings.ui'

  def ui_filepath(self):
    return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())