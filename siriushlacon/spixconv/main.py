#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydm import Display

from siriushlacon.spixconv.consts import SPIXCONV_MAIN


class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(parent=parent, args=args,
            macros=macros, ui_filename=SPIXCONV_MAIN)

        # defining macros for PyDMShellCommand
        #self.***object_name***.macros = json.dumps({"pv_prefix":"TB-04:PU-InjSept"})
        #self.***object_name***.macros = json.dumps({"pv_prefix":"BO-01D:PU-InjKckr"})

