#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pkg_resources


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


# Images
CHECK_IMG = get_abs_path("images/check.png")
CNPEM_IMG = get_abs_path("images/CNPEM.jpg")
LNLS_IMG = get_abs_path("images/LNLS.png")
PLAY_IMG = get_abs_path("images/play_button.jpg")
STOP_IMG = get_abs_path("images/stop_button.jpg")
WARNING_IMG = get_abs_path("images/warning.png")

# UI
ADVANCED_WINDOW_UI = get_abs_path("ui/advanced_window.ui")
CONFIRMATION_MESSAGE = get_abs_path("ui/confirmation_message.ui")
MAIN_WINDOW_UI = get_abs_path("ui/main_window.ui")
OK_MESSAE_UI = get_abs_path("ui/OK_message.ui")
SYSTEM_WINDOW_UI = get_abs_path("ui/system_window.ui")
WARNING_WINDOW_UI = get_abs_path("ui/warning_message.ui")

# Scripts
CHECK_PRESSURE_SCRIPT = get_abs_path("scripts/check_pressure.py")
CLEAN_STATUS_SCRIPT = get_abs_path("scripts/clean_status_PV.py")
COMMUTE_VALVE_SCRIPT = get_abs_path("scripts/commute_valve.py")
PROCESS_OFF_SCRIPT = get_abs_path("scripts/process_off.py")
PROCESS_ON_SCRIPT = get_abs_path("scripts/process_on.py")
PROCESS_RECOVERYY_SCRIPT = get_abs_path("scripts/process_recovery.py")
