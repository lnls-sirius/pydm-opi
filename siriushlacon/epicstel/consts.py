#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pkg_resources


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


EPICSTEL_MAIN = get_abs_path("main.py")
EPICSTEL_MAIN_UI = get_abs_path("ui/main.ui")
EPICSTEL_LOGIN_UI = get_abs_path("ui/login.ui")
EPICSTEL_GROUP_UI = get_abs_path("ui/group.ui")

EPICSTEL_SERVER = "10.0.38.46"
EPICSTEL_SERVER_USER = ""
EPICSTEL_SERVER_PASS = ""

EPICSTEL_LOCATION = "/storage/services/repository/telegrampy/Data/"
