#!/usr/bin/env python3
import enum

import pkg_resources

BBB_IOC_ADDR = [
    "10.128.40.1:5064",
    "10.128.40.1:5068",
    "10.128.40.2:5064",
    "10.128.40.2:5068",
    "10.128.40.3:5064",
    "10.128.40.3:5068",
    "10.128.40.4:5064",
    "10.128.40.4:5068",
    "10.128.40.5:5064",
    "10.128.40.5:5068",
    "10.128.40.6:5064",
    "10.128.40.6:5068",
    "10.128.40.7:5064",
    "10.128.40.7:5068",
    "10.128.40.8:5064",
    "10.128.40.8:5068",
    "10.128.40.9:5064",
    "10.128.40.9:5068",
    "10.128.40.10:5064",
    "10.128.40.10:5068",
]


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


class Finished(str, enum.Enum):
    ON = "ON"
    OFF = "OFF"
    REC = "REC"


# Images
CHECK_IMG = get_abs_path("resources/images/check.png")
CNPEM_IMG = get_abs_path("resources/images/CNPEM.jpg")
LNLS_IMG = get_abs_path("resources/images/LNLS.png")
PLAY_IMG = get_abs_path("resources/images/play_button.jpg")
STOP_IMG = get_abs_path("resources/images/stop_button.png")
WARNING_IMG = get_abs_path("resources/images/warning.png")

# UI
ADVANCED_WINDOW_UI = get_abs_path("resources/ui/advanced_window.ui")
CONFIRMATION_MESSAGE_UI = get_abs_path("resources/ui/confirmation_message.ui")
MAIN_WINDOW_UI = get_abs_path("resources/ui/main_window.ui")
OK_MESSAGE_UI = get_abs_path("resources/ui/OK_message.ui")
SYSTEM_WINDOW_UI = get_abs_path("resources/ui/system_window.ui")
WARNING_WINDOW_UI = get_abs_path("resources/ui/warning_message.ui")
SIMPLE_WINDOW_UI = get_abs_path("resources/ui/simple_window.ui")

# PY
ADVANCED_WINDOW_PY = get_abs_path("advanced_window.py")
CONFIRMATION_MESSAGE_PY = get_abs_path("confirmation_message.py")
MAIN_WINDOW_PY = get_abs_path("main_window.py")
OK_MESSAGE_PY = get_abs_path("OK_message.py")
SYSTEM_WINDOW_PY = get_abs_path("system_window.py")
WARNING_WINDOW_PY = get_abs_path("warning_message.py")
SIMPLE_WINDOW_PY = get_abs_path("simple_window.py")
