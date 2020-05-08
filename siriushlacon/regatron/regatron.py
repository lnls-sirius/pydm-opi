import logging
import json

from pydm import Display
from pydm.utilities import IconFont
from pydm.widgets.channel import PyDMChannel

from siriushlacon.regatron.consts import (
    COMPLETE_UI,
    ERR_MAIN,
    WARN_MAIN,
    EXTENDED_MAP,
    STANDARD_MAP,
    ALARM_MAIN,
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

        self.btnErr.filenames = [ERR_MAIN]
        self.btnWarn.filenames = [WARN_MAIN]

        self.btnSysHistory.filenames = [ALARM_MAIN]
        self.btnSysHistory.macros = json.dumps({"P": macros["P"], "T": "Sys"})
        self.btnModHistory.filenames = [ALARM_MAIN]
        self.btnModHistory.macros = json.dumps({"P": macros["P"], "T": "Mod"})

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
        self.btnMMV.setIcon(REFRESH_ICON)
        self.btnMMC.setIcon(REFRESH_ICON)
        self.btnMMinC.setIcon(REFRESH_ICON)
        self.btnMMP.setIcon(REFRESH_ICON)
        self.btnMMinV.setIcon(REFRESH_ICON)
        self.btnMMinP.setIcon(REFRESH_ICON)
        self.btnMRes.setIcon(REFRESH_ICON)
        self.btnNomDCV.setIcon(REFRESH_ICON)
        self.btnDCV.setIcon(REFRESH_ICON)
        self.btnMOV.setIcon(REFRESH_ICON)
        self.btnMOC.setIcon(REFRESH_ICON)
        self.btnMOP.setIcon(REFRESH_ICON)

        self.btnMVPRb.setIcon(REFRESH_ICON)
        self.btnMVLQ4Rb.setIcon(REFRESH_ICON)
        self.btnMCPRb.setIcon(REFRESH_ICON)
        self.btnMCQLRb.setIcon(REFRESH_ICON)
        self.btnMPPRb.setIcon(REFRESH_ICON)
        self.btnMPLQRb.setIcon(REFRESH_ICON)
        self.btnMRPRb.setIcon(REFRESH_ICON)

        # System
        self.PyDMPushButton_17.setIcon(REFRESH_ICON)
        self.PyDMPushButton_18.setIcon(REFRESH_ICON)
        self.PyDMPushButton_19.setIcon(REFRESH_ICON)
        self.PyDMPushButton_20.setIcon(REFRESH_ICON)
        self.PyDMPushButton_21.setIcon(REFRESH_ICON)
        self.PyDMPushButton_22.setIcon(REFRESH_ICON)
        self.PyDMPushButton_23.setIcon(REFRESH_ICON)
        self.PyDMPushButton_28.setIcon(REFRESH_ICON)
        self.PyDMPushButton_29.setIcon(REFRESH_ICON)
        self.PyDMPushButton_45.setIcon(REFRESH_ICON)
        self.PyDMPushButton_46.setIcon(REFRESH_ICON)
        self.PyDMPushButton_47.setIcon(REFRESH_ICON)
        self.PyDMPushButton_48.setIcon(REFRESH_ICON)
        self.PyDMPushButton_49.setIcon(REFRESH_ICON)
        self.PyDMPushButton_57.setIcon(REFRESH_ICON)
        self.PyDMPushButton_71.setIcon(REFRESH_ICON)
        self.PyDMPushButton_73.setIcon(REFRESH_ICON)

        # Advanced
        self.PyDMPushButton_41.setIcon(REFRESH_ICON)
        self.PyDMPushButton_50.setIcon(REFRESH_ICON)
        self.PyDMPushButton_51.setIcon(REFRESH_ICON)
        self.PyDMPushButton_52.setIcon(REFRESH_ICON)
