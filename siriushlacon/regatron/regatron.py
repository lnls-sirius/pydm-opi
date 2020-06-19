import logging
import json

import epics

from pydm import Display
from pydm.utilities import IconFont
from pydm.widgets.channel import PyDMChannel
from qtpy.QtWidgets import QTableWidgetItem

from siriushlacon.regatron.consts import (
    COMPLETE_UI,
    TREE_32,
    READINGS_MAP,
    ALARM_MAIN,
    CODES,
)

logger = logging.getLogger()


class ProtectionLevel(object):
    OPERATION = 0
    ADVANCED = 1


class Regatron(Display):
    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, macros=macros, ui_filename=COMPLETE_UI)
        self.macros = macros

        self.protectionLevel: ProtectionLevel = ProtectionLevel.OPERATION
        self.setup_icons()

        self.btnModHistory.filenames = [ALARM_MAIN]
        self.btnModHistory.macros = [json.dumps({"T": "Mod", "P": macros["P"]})]
        self.btnModHistory.openInNewWindow = True

        self.btnSysHistory.filenames = [ALARM_MAIN]
        self.btnSysHistory.macros = [json.dumps({"T": "Sys", "P": macros["P"]})]
        self.btnSysHistory.openInNewWindow = True

        self.btnModWarn.filenames = [TREE_32]
        self.btnSysWarn.filenames = [TREE_32]
        self.btnModErr.filenames = [TREE_32]
        self.btnSysErr.filenames = [TREE_32]

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

        # Flash Error History
        # self.ch_flash_error_history = PyDMChannel(
        #    address="ca://" + macros["P"] + ":ErrorHistory-Mon",
        #    value_slot=self.flash_error_history,
        # )
        # @todo: do this better !
        self.flashHistoryTable.verticalHeader().setVisible(False)

        self.errorHistoryPV = epics.PV(
            pvname="{}{}".format(macros["P"], ":ErrorHistory-Mon"),
            callback=self.flash_error_history,
        )
        try:
            self.flash_error_history(self.errorHistoryPV.value)
        except:
            pass
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

    def get_group_string(self, group_):
        group = int(group_)

        for k, v in READINGS_MAP.items():
            if (group >> k) == 1:
                return "{}) {}".format(CODES[k], v)
        return "{:X}) ?".format(group)

    def get_code_string(self, code_):
        code = int(code_)

        for k in range(32):
            if (code >> k) == 1:
                return "{}".format(CODES[k])
        return "{}?".format(code)

    def flash_error_history(self, *args, **kwargs):
        if not kwargs["value"]:
            return

        self.flashHistoryTable.clearContents()
        values = kwargs["value"][:-1]
        data = []

        self.flashHistoryTable.setRowCount(len(values))
        i = 0
        for value in values:
            n, day, hour, minute, second, milli, group, code = value.split(",")

            self.flashHistoryTable.setItem(i, 0, QTableWidgetItem(n))
            self.flashHistoryTable.setItem(i, 1, QTableWidgetItem(day))
            self.flashHistoryTable.setItem(i, 2, QTableWidgetItem(hour))
            self.flashHistoryTable.setItem(i, 3, QTableWidgetItem(minute))
            self.flashHistoryTable.setItem(i, 4, QTableWidgetItem(milli))
            self.flashHistoryTable.setItem(
                i, 5, QTableWidgetItem(self.get_group_string(group))
            )
            self.flashHistoryTable.setItem(
                i, 6, QTableWidgetItem(self.get_code_string(code))
            )
            i += 1

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
