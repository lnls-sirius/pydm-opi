#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from pydm import Display

import json
from PyQt5.QtGui import QColor

class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(parent=parent, args=args, macros=macros)

        # defining macros for PyDMRelatedDisplayButton (for opening "system_window.ui")
        self.VBC_car_1.macros = json.dumps({"IOC": "VBC1", "CAR": "1"})
        self.VBC_car_2.macros = json.dumps({"IOC": "VBC2", "CAR": "2"})
        self.VBC_car_3.macros = json.dumps({"IOC": "VBC3", "CAR": "3"})
        self.VBC_car_4.macros = json.dumps({"IOC": "VBC4", "CAR": "4"})
        self.VBC_car_5.macros = json.dumps({"IOC": "VBC5", "CAR": "5"})
        self.VBC_car_6.macros = json.dumps({"IOC": "VBC6", "CAR": "6"})
        self.VBC_car_7.macros = json.dumps({"IOC": "VBC7", "CAR": "7"})
        self.VBC_car_8.macros = json.dumps({"IOC": "VBC8", "CAR": "8"})
        self.VBC_car_9.macros = json.dumps({"IOC": "VBC9", "CAR": "9"})
        self.VBC_car_10.macros = json.dumps({"IOC": "VBC10", "CAR": "10"})

        self.LED_1._disconnected_color = QColor(255, 0, 0)
        self.LED_2._disconnected_color = QColor(255, 0, 0)
        self.LED_3._disconnected_color = QColor(255, 0, 0)
        self.LED_4._disconnected_color = QColor(255, 0, 0)
        self.LED_5._disconnected_color = QColor(255, 0, 0)
        self.LED_6._disconnected_color = QColor(255, 0, 0)
        self.LED_7._disconnected_color = QColor(255, 0, 0)
        self.LED_8._disconnected_color = QColor(255, 0, 0)
        self.LED_9._disconnected_color = QColor(255, 0, 0)
        self.LED_10._disconnected_color = QColor(255, 0, 0)

    def ui_filename(self):
        return '../ui/latest/main_window.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
