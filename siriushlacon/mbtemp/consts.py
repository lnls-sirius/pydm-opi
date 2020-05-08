#!/usr/bin/env python3

import logging
import pkg_resources

import conscommon.data
import conscommon.data_model

logger = logging.getLogger()


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


MBTEMP_MAIN = get_abs_path("main.py")
MBTEMP_MAIN_UI = get_abs_path("ui/main.ui")

DEVICES = conscommon.data_model.getDevicesFromBeagles(
    conscommon.data_model.getBeaglesFromList(conscommon.data.getMBTemp())
)
