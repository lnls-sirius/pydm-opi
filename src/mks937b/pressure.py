#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydm import Display

from src.consts.mks937b import COLD_CATHODE
from src.paths import get_abs_path, PRESSURE_UI, IS_LINUX


class Pressure(Display):

    def __init__(self, parent=None, args=[], macros=None):
        super(Pressure, self).__init__(parent=parent, args=args, macros=macros)
        # if IS_LINUX:
        #     self.tpA1.setLogMode(False, True)
        #     self.tpA2.setLogMode(False, True)
        #     self.tpB1.setLogMode(False, True)
        #     self.tpB2.setLogMode(False, True)
        #     self.tpC1.setLogMode(False, True)
        #     self.tpC2.setLogMode(False, True)

        if macros:
            if macros.get('A') == COLD_CATHODE:
                self.alarm2.hide()
                self.lblA2.hide()
                self.cbA2.hide()
                self.biA2.hide()
                self.plblA2.hide()
                if IS_LINUX:
                    self.tpA2.hide()

            if macros.get('B') == COLD_CATHODE:
                self.lblB2.hide()
                self.alarm4.hide()
                self.lblA2.hide()
                self.cbB2.hide()
                self.biB2.hide()
                self.plblB2.hide()
                if IS_LINUX:
                    self.tpB2.hide()

            if macros.get('C') == COLD_CATHODE:
                self.lblC2.hide()
                self.alarm6.hide()
                self.lblA2.hide()
                self.cbC2.hide()
                self.biC2.hide()
                self.plblC2.hide()
                if IS_LINUX:
                    self.tpC2.hide()

    def ui_filename(self):
        return PRESSURE_UI

    def ui_filepath(self):
        return get_abs_path(PRESSURE_UI)
