import logging
from pydm import Display
from pydm.utilities import IconFont
from pydm.widgets.channel import PyDMChannel
from qtpy.QtWidgets import QTableWidgetItem

from siriushlacon.regatron.consts import (
    COMPLETE_UI,
    TREE_32_UI,
    READINGS_MAP,
    ALARM_MAIN,
)

logger = logging.getLogger()


def get_report(value, msg):
    erros = []
    for k, v in READINGS_MAP.items():
        if value & (1 << k):
            erros.append(v)
    logger.info("{} {}".format(msg, erros))
    return erros


class AlarmTree(Display):
    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, macros=macros, ui_filename=TREE_32_UI)

        self.isSystem = macros.get("D", "Sys") == "Sys"
        self.isWarn = macros.get("T", "Warn") == "Warn"

        # Warning Groups
        self.ch_mod_warn_report = PyDMChannel(
            address="ca://" + macros["P"] + ":ModWarnGroup-Mon",
            value_slot=self.get_mod_warn_report,
        )

        self.ch_sys_warn_report = PyDMChannel(
            address="ca://" + macros["P"] + ":SysWarnGroup-Mon",
            value_slot=self.get_sys_warn_report,
        )

        # Error Groups
        self.ch_mod_error_report = PyDMChannel(
            address="ca://" + macros["P"] + ":ModErrGroup-Mon",
            value_slot=self.get_mod_error_report,
        )

        self.ch_sys_error_report = PyDMChannel(
            address="ca://" + macros["P"] + ":SysErrGroup-Mon",
            value_slot=self.get_sys_error_report,
        )

        if self.isSystem:
            if self.isWarn:
                self.ch_sys_warn_report.connect()
            else:
                self.ch_sys_error_report.connect()
        else:
            if self.isWarn:
                self.ch_mod_warn_report.connect()
            else:
                self.ch_mod_error_report.connect()

    # Warning
    def get_mod_warn_report(self, value):
        self.label.setText("\n".join(get_report(value, "Module")))

    def get_sys_warn_report(self, value):
        self.label.setText("\n".join(get_report(value, "System")))

    # Error
    def get_mod_error_report(self, value):
        self.label.setText("\n".join(get_report(value, "Module")))

    def get_sys_error_report(self, value):
        self.label.setText("\n".join(get_report(value, "System")))
