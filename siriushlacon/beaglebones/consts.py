#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pkg_resources


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


BEAGLEBONES_MAIN = get_abs_path("main.py")
BEAGLEBONES_MAIN_UI = get_abs_path("ui/main.ui")

INFO_BBB_UI = get_abs_path("ui/infoBBB.ui")
CHANGE_BBB_UI = get_abs_path("ui/configBBB.ui")
LOGS_BBB_UI = get_abs_path("ui/logsBBB.ui")

RED_LED = get_abs_path("ui/Resources/led-red.png")
GREEN_LED = get_abs_path("ui/Resources/led-green.png")
