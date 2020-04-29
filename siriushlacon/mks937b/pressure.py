#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydm import Display
from conscommon.data_model.mks import MKS_SENSOR_COLD_CATHODE
from siriushlacon.mks937b.consts import PRESSURE_UI
from siriushlacon.utils.consts import IS_LINUX


class Pressure(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(Pressure, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=PRESSURE_UI
        )

        if macros:
            if macros.get("A") == MKS_SENSOR_COLD_CATHODE:
                self.alarm2.hide()
                self.lblA2.hide()
                self.cbA2.hide()
                self.biA2.hide()
                self.plblA2.hide()
                if IS_LINUX:
                    self.tpA2.hide()

            if macros.get("B") == MKS_SENSOR_COLD_CATHODE:
                self.lblB2.hide()
                self.alarm4.hide()
                self.lblA2.hide()
                self.cbB2.hide()
                self.biB2.hide()
                self.plblB2.hide()
                if IS_LINUX:
                    self.tpB2.hide()

            if macros.get("C") == MKS_SENSOR_COLD_CATHODE:
                self.lblC2.hide()
                self.alarm6.hide()
                self.lblA2.hide()
                self.cbC2.hide()
                self.biC2.hide()
                self.plblC2.hide()
                if IS_LINUX:
                    self.tpC2.hide()
