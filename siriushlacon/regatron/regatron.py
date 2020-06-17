import logging
import json

from pydm import Display
from pydm.utilities import IconFont
from pydm.widgets.channel import PyDMChannel

from siriushlacon.regatron.consts import (
    COMPLETE_UI,
    TREE_32_UI,
    READINGS_MAP,
    READINGS,
    ALARM_MAIN,
)

logger = logging.getLogger()


def get_report(value, msg):
    erros = []
    for k, v in READINGS_MAP.items():
        if value & 1 << k:
            erros.append(v)
    logger.info("{} {}".format(msg, erros))
    return erros


class ProtectionLevel(object):
    OPERATION = 0
    ADVANCED = 1


class Regatron(Display):
    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, macros=macros, ui_filename=COMPLETE_UI)
        self.macros = macros

        self.protectionLevel: ProtectionLevel = ProtectionLevel.OPERATION
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
        self.ch_mod_warn_report = PyDMChannel(
            address="ca://" + macros["P"] + ":Mod-WarnGroup-Mon",
            value_slot=self.get_mod_warn_report,
        )
        self.ch_mod_warn_report.connect()

        self.ch_sys_warn_report = PyDMChannel(
            address="ca://" + macros["P"] + ":Sys-WarnGroup-Mon",
            value_slot=self.get_sys_warn_report,
        )
        self.ch_sys_warn_report.connect()

        # Error Groups
        self.ch_mod_error_report = PyDMChannel(
            address="ca://" + macros["P"] + ":Mod-ErrGroup-Mon",
            value_slot=self.get_mod_error_report,
        )
        self.ch_mod_error_report.connect()

        self.ch_sys_error_report = PyDMChannel(
            address="ca://" + macros["P"] + ":Sys-ErrGroup-Mon",
            value_slot=self.get_sys_error_report,
        )
        self.ch_sys_error_report.connect()
        # ----------------------------------------------

        self.btnProtectionLevel.passwordProtected = True
        self.btnProtectionLevel.password = "ELPS"
        self.btnProtectionLevel.clicked.connect(self.changeProtectionLevel)
        self.btnProtectionLevel.setText(
            "OPERATION"
            if self.protectionLevel == ProtectionLevel.OPERATION
            else "ADVANCED"
        )
        self.changeItemProtection(
            unlock=True if self.protectionLevel == ProtectionLevel.ADVANCED else False
        )

        self.lblTitle.setText(
            "{} - {}".format(
                macros["P"], "Master" if macros.get("master", "1") == "1" else "slave"
            )
        )
        self.configWidget(isMaster=macros.get("master", "1") == "1")

        self.slopeVoltageMax = PyDMChannel(
            address="ca://" + macros["P"] + ":Sys-SlopeVoltMax-Mon",
            value_slot=self.voltageSlopeMaxChanged,
        )
        self.slopeVoltageMin = PyDMChannel(
            address="ca://" + macros["P"] + ":Sys-SlopeVoltMin-Mon",
            value_slot=self.voltageSlopeMinChanged,
        )
        self.slopeVoltageMax.connect()
        self.slopeVoltageMin.connect()

        self.slopeCurrentMax = PyDMChannel(
            address="ca://" + macros["P"] + ":Sys-SlopeCurrMax-Mon",
            value_slot=self.currentSlopeMaxChanged,
        )
        self.slopeCurrentMin = PyDMChannel(
            address="ca://" + macros["P"] + ":Sys-SlopeCurrMin-Mon",
            value_slot=self.currentSlopeMinChanged,
        )
        self.slopeCurrentMax.connect()
        self.slopeCurrentMin.connect()

    def voltageSlopeMaxChanged(self, value):
        self.spbxSlopeVoltSp.setMaximum(value)
        self.spbxSlopeStartupVoltSp.setMaximum(value)

    def voltageSlopeMinChanged(self, value):
        self.spbxSlopeVoltSp.setMinimum(value)
        self.spbxSlopeVoltSp.setSingleStep(value)

        self.spbxSlopeStartupVoltSp.setMinimum(value)
        self.spbxSlopeStartupVoltSp.setSingleStep(value)

    def currentSlopeMaxChanged(self, value):
        self.spbxSlopeCurrSp.setMaximum(value)
        self.spbxSlopeStartupCurrSp.setMaximum(value)

    def currentSlopeMinChanged(self, value):
        self.spbxSlopeCurrSp.setMinimum(value)
        self.spbxSlopeCurrSp.setSingleStep(value)

        self.spbxSlopeStartupCurrSp.setMinimum(value)
        self.spbxSlopeStartupCurrSp.setSingleStep(value)

    def configWidget(self, isMaster):
        self.sysFrame.setVisible(isMaster)
        self.btnSysErr.setVisible(isMaster)
        self.btnSysWarn.setVisible(isMaster)
        self.btnClear.setVisible(isMaster)

        self.warnByte.channel = "ca://{}{}".format(
            self.macros["P"], ":GenWarn-Mon" if isMaster else ":Mod-WarnGroup-Mon",
        )
        self.errorByte.channel = "ca://{}{}".format(
            self.macros["P"], ":GenErr-Mon" if isMaster else ":Mod-ErrGroup-Mon",
        )

    def changeProtectionLevel(self):

        if (
            self.protectionLevel == ProtectionLevel.OPERATION
            and self.btnProtectionLevel.validate_password()
        ):
            self.protectionLevel = ProtectionLevel.ADVANCED

        elif self.protectionLevel == ProtectionLevel.ADVANCED:
            # Lock things up ! No need for password prompt
            self.protectionLevel = ProtectionLevel.OPERATION

        self.btnProtectionLevel.setText(
            "OPERATION"
            if self.protectionLevel == ProtectionLevel.OPERATION
            else "ADVANCED"
        )
        self.changeItemProtection(
            unlock=True if self.protectionLevel == ProtectionLevel.ADVANCED else False
        )

    def changeItemProtection(self, unlock):
        self.tabWidget.setTabEnabled(1, unlock)
        self.tabWidget.setTabEnabled(2, unlock)
        self.tabWidget.setTabEnabled(3, unlock)
        self.tabWidget.setTabEnabled(4, unlock)

        self.btnSave.setEnabled(unlock)
        self.leSysVoltRefSp.setEnabled(unlock)
        self.leSysCurrRefSp.setEnabled(unlock)
        self.leSysPwrRefSp.setEnabled(unlock)
        self.leSysResRefSp.setEnabled(unlock)

        self.btnSave.setVisible(unlock)
        self.leSysVoltRefSp.setVisible(unlock)
        self.leSysCurrRefSp.setVisible(unlock)
        self.leSysPwrRefSp.setVisible(unlock)
        self.leSysResRefSp.setVisible(unlock)

    # Warning
    def get_mod_warn_report(self, value):
        self.lblModGenWarnStd.setText("\n".join(get_report(value, "Module")))

    def get_sys_warn_report(self, value):
        self.lblSysGenWarnStd.setText("\n".join(get_report(value, "System")))

    # Error
    def get_mod_error_report(self, value):
        self.lblModGenErrStd.setText("\n".join(get_report(value, "Module")))

    def get_sys_error_report(self, value):
        self.lblSysGenErrStd.setText("\n".join(get_report(value, "System")))

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
        self.btnSysVoltRef_2.setIcon(REFRESH_ICON)
        self.btnSysCurrRef_2.setIcon(REFRESH_ICON)
        self.btnSysResRef_2.setIcon(REFRESH_ICON)
        self.btnSysPwrRef_2.setIcon(REFRESH_ICON)

        self.btnVoltSlope.setIcon(REFRESH_ICON)
        self.btnCurrSlope.setIcon(REFRESH_ICON)

        # Advanced
