#!/usr/bin/env python3

import logging
import pkg_resources

import conscommon.data

from siriushlacon.utils import LazyDevices

logger = logging.getLogger()


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


MBTEMP_MAIN = get_abs_path("main.py")
MBTEMP_MAIN_UI = get_abs_path("ui/main.ui")

lazy_devices = LazyDevices(conscommon.data.getMBTemp)
