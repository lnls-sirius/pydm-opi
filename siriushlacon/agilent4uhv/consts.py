#!/usr/bin/env python3
import pkg_resources

import conscommon.data

from siriushlacon.utils import LazyDevices


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


AGILENT_OVERVIEW = get_abs_path("overview.py")

AGILENT_MAIN = get_abs_path("main.py")
AGILENT_MAIN_UI = get_abs_path("ui/main.ui")

AGILENT_DEVICE_MAIN = get_abs_path("device_main.py")
AGILENT_DEVICE_MAIN_UI = get_abs_path("ui/device_main.ui")

AGILENT_DEVICE = get_abs_path("device.py")
AGILENT_DEVICE_UI = get_abs_path("ui/device.ui")

AGILENT_CHANNEL = get_abs_path("channel.py")
AGILENT_CHANNEL_UI = get_abs_path("ui/channel.ui")

AGILENT_EXTENDED = get_abs_path("extended.py")


lazy_devices = LazyDevices(conscommon.data.getAgilent)
