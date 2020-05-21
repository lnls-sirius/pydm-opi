import logging
import json

from pydm import Display
from pydm.utilities import IconFont
from pydm.widgets.channel import PyDMChannel

from siriushlacon.regatron.consts import (
    COMPLETE_UI,
    TREE_32_UI,
    EXTENDED_MAP,
    STANDARD_MAP,
)

logger = logging.getLogger()


def get_report(value, map_, msg):
    erros = []
    for k, v in map_.items():
        if value & 1 << k:
            erros.append(v)
    logger.info("{} {}".format(msg, erros))
    return erros


class Regatron(Display):
    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, macros=macros, ui_filename=COMPLETE_UI)
        self.setup_icons()

        self.btnModWarn.filenames = [TREE_32_UI]
        self.btnSysWarn.filenames = [TREE_32_UI]
        self.btnModErr.filenames = [TREE_32_UI]
        self.btnSysErr.filenames = [TREE_32_UI]

        self.btnModWarn.macros = json.dumps(
            {"Title": "Module Warnings", "P": macros["P"], "D": "Mod", "T": "Warn"}
        )
        self.btnSysWarn.macros = json.dumps(
            {"Title": "System Warnings", "P": macros["P"], "D": "Sys", "T": "Warn"}
        )
        self.btnModErr.macros = json.dumps(
            {"Title": "Module Error", "P": macros["P"], "D": "Mod", "T": "Err"}
        )
        self.btnSysErr.macros = json.dumps(
            {"Title": "System Error", "P": macros["P"], "D": "Sys", "T": "Err"}
        )

        # Warning Groups
        self.ch_mod_std_warn_report = PyDMChannel(
            address="ca://" + macros["P"] + ":Mod-StdWarnGroup-Mon",
            value_slot=self.get_mod_std_warn_report,
        )
        self.ch_mod_std_warn_report.connect()

        self.ch_sys_std_warn_report = PyDMChannel(
            address="ca://" + macros["P"] + ":Sys-StdWarnGroup-Mon",
            value_slot=self.get_sys_std_warn_report,
        )
        self.ch_sys_std_warn_report.connect()

        self.ch_mod_ext_warn_report = PyDMChannel(
            address="ca://" + macros["P"] + ":Mod-ExtWarnGroup-Mon",
            value_slot=self.get_mod_ext_warn_report,
        )
        self.ch_mod_ext_warn_report.connect()

        self.ch_sys_ext_warn_report = PyDMChannel(
            address="ca://" + macros["P"] + ":Sys-ExtWarnGroup-Mon",
            value_slot=self.get_sys_ext_warn_report,
        )
        self.ch_sys_ext_warn_report.connect()

        # Error Groups
        self.ch_mod_std_error_report = PyDMChannel(
            address="ca://" + macros["P"] + ":Mod-StdErrGroup-Mon",
            value_slot=self.get_mod_std_error_report,
        )
        self.ch_mod_std_error_report.connect()

        self.ch_sys_std_error_report = PyDMChannel(
            address="ca://" + macros["P"] + ":Sys-StdErrGroup-Mon",
            value_slot=self.get_sys_std_error_report,
        )
        self.ch_sys_std_error_report.connect()

        self.ch_mod_ext_error_report = PyDMChannel(
            address="ca://" + macros["P"] + ":Mod-ExtErrGroup-Mon",
            value_slot=self.get_mod_ext_error_report,
        )
        self.ch_mod_std_error_report.connect()

        self.ch_sys_ext_error_report = PyDMChannel(
            address="ca://" + macros["P"] + ":Sys-ExtErrGroup-Mon",
            value_slot=self.get_sys_ext_error_report,
        )
        self.ch_sys_ext_error_report.connect()

    # Warning
    def get_mod_ext_warn_report(self, value):
        self.lblModGenWarnExt.setText(
            "\n".join(get_report(value, EXTENDED_MAP, "Module extended"))
        )

    def get_sys_ext_warn_report(self, value):
        self.lblSysGenWarnExt.setText(
            "\n".join(get_report(value, EXTENDED_MAP, "System extended"))
        )

    def get_mod_std_warn_report(self, value):
        self.lblModGenWarnStd.setText(
            "\n".join(get_report(value, STANDARD_MAP, "Module standard"))
        )

    def get_sys_std_warn_report(self, value):
        self.lblSysGenWarnStd.setText(
            "\n".join(get_report(value, STANDARD_MAP, "System standard"))
        )

    # Error
    def get_mod_std_error_report(self, value):
        self.lblModGenErrStd.setText(
            "\n".join(get_report(value, STANDARD_MAP, "Module standard"))
        )

    def get_mod_ext_error_report(self, value):
        self.lblModGenErrExt.setText(
            "\n".join(get_report(value, EXTENDED_MAP, "Module extended"))
        )

    def get_sys_std_error_report(self, value):
        self.lblSysGenErrStd.setText(
            "\n".join(get_report(value, STANDARD_MAP, "System standard"))
        )

    def get_sys_ext_error_report(self, value):
        self.lblSysGenErrExt.setText(
            "\n".join(get_report(value, EXTENDED_MAP, "System extended"))
        )

    def setup_icons(self):
        REFRESH_ICON = IconFont().icon("refresh")
        # Overview
        self.btnSstate.setIcon(REFRESH_ICON)
        self.btnSCtrlMode.setIcon(REFRESH_ICON)
        self.btnMState.setIcon(REFRESH_ICON)
        self.btnMCtrlMode.setIcon(REFRESH_ICON)
        self.btnActIFace.setIcon(REFRESH_ICON)

        self.btnSave.setIcon(IconFont().icon("download"))
        self.btnClear.setIcon(IconFont().icon("eraser"))

        # Module
        # System
        self.btnSysVoltRef.setIcon(REFRESH_ICON)
        self.btnSysCurrRef.setIcon(REFRESH_ICON)
        self.btnSysResRef.setIcon(REFRESH_ICON)
        self.btnSysPwrRef.setIcon(REFRESH_ICON)
        self.btnVoltSlope.setIcon(REFRESH_ICON)
        self.btnCurrSlope.setIcon(REFRESH_ICON)

        # Advanced
