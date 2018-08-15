#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from pydm import Display
from pydm.widgets import PyDMTimePlot

from consts import COLD_CATHODE, PIRANI

class Pressure(Display):
  def __init__(self, parent=None, args=[], macros=None):
    super(Pressure, self).__init__(parent=parent, args=args, macros=macros)

    if macros:
        if macros.get('A') == COLD_CATHODE:
            self.lblA2.hide()
            self.cbA2.hide()
            self.biA2.hide()
            self.plblA2.hide()
            self.tpA2.hide()
        elif macros.get('A') == PIRANI:
            pass

        if macros.get('B') == COLD_CATHODE:
            self.lblB2.hide()
            self.cbB2.hide()
            self.biB2.hide()
            self.plblB2.hide()
            self.tpB2.hide()
        elif macros.get('B') == PIRANI:
            pass

        if macros.get('C') == COLD_CATHODE:
            self.lblC2.hide()
            self.cbC2.hide()
            self.biC2.hide()
            self.plblC2.hide()
            self.tpC2.hide()
        elif macros.get('C') == PIRANI:
            pass

  def ui_filename(self):
    return '../ui/pressure.ui'

  def ui_filepath(self):
    return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())