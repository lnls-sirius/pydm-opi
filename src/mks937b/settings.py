#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from pydm import Display

from src.mks937b.consts import COLD_CATHODE, PIRANI, CC_UI, PR_UI, SETTINGS_UI
from src.mks937b.macros import get_macro


class Settings(Display):

    def __init__(self, parent=None, args=[], macros=None):
        super(Settings, self).__init__(parent=parent, args=args, macros=macros)

        self.pdispA.macros = json.dumps(
            get_macro(macros.get('DEVICE'),
                      'A',
                      macros.get('G1'),
                      macros.get('G2')))
        self.pdispB.macros = json.dumps(
            get_macro(macros.get('DEVICE'),
                      'B',
                      macros.get('G3'),
                      macros.get('G4')))
        self.pdispC.macros = json.dumps(
            get_macro(macros.get('DEVICE'),
                      'C',
                      macros.get('G5'),
                      macros.get('G6')))

        if macros:
            if macros.get('A') == COLD_CATHODE:
                self.pdispA.filename = CC_UI
            elif macros.get('A') == PIRANI:
                self.pdispA.filename = PR_UI

            if macros.get('B') == COLD_CATHODE:
                self.pdispB.filename = CC_UI
            elif macros.get('B') == PIRANI:
                self.pdispB.filename = PR_UI

            if macros.get('C') == COLD_CATHODE:
                self.pdispC.filename = CC_UI
            elif macros.get('C') == PIRANI:
                self.pdispC.filename = PR_UI

        self.pdispA.setAutoFillBackground(False)
        self.pdispB.setAutoFillBackground(False)
        self.pdispC.setAutoFillBackground(False)

    def ui_filename(self):
        return SETTINGS_UI

    def ui_filepath(self):
        return SETTINGS_UI
