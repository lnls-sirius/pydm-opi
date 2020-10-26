import logging
import json
import datetime

import epics

from pydm import Display
from pydm.utilities import IconFont
from pydm.widgets.channel import PyDMChannel
from qtpy.QtWidgets import QTableWidgetItem
from qtpy.QtGui import QDesktopServices
from qtpy.QtCore import QUrl

from siriushlacon.regatron.consts import (
    COMPLETE_UI,
    TREE_32,
    READINGS_MAP,
    ALARM_MAIN,
    CODES,
    ERROR_LIST_PDF,
)

logger = logging.getLogger()


class ProtectionLevel(object):
    OPERATION = 0
    ADVANCED = 1


class TabId(object):
    Overview = 0
    System = 1
    Module = 2
    ErrWarn = 3
    Advanced = 4


class Regatron(Display):
    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, macros=macros, ui_filename=COMPLETE_UI)
        self.macros_dict = macros
        self.isMaster = macros.get("master", "1") == "1"

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
        self.configWidget()

        self.slopeVoltageMax = PyDMChannel(
            address="ca://" + macros["P"] + ":SysSlopeVoltMax-Mon",
            value_slot=self.voltageSlopeMaxChanged,
        )
        self.slopeVoltageMin = PyDMChannel(
            address="ca://" + macros["P"] + ":SysSlopeVoltMin-Mon",
            value_slot=self.voltageSlopeMinChanged,
        )
        self.slopeVoltageMax.connect()
        self.slopeVoltageMin.connect()

        self.slopeCurrentMax = PyDMChannel(
            address="ca://" + macros["P"] + ":SysSlopeCurrMax-Mon",
            value_slot=self.currentSlopeMaxChanged,
        )
        self.slopeCurrentMin = PyDMChannel(
            address="ca://" + macros["P"] + ":SysSlopeCurrMin-Mon",
            value_slot=self.currentSlopeMinChanged,
        )
        self.slopeCurrentMax.connect()
        self.slopeCurrentMin.connect()

        self.modStatusPV = PyDMChannel(
            address="ca://{}{}".format(macros["P"], ":ModState-Mon"),
            value_slot=self.update_mod_state_label,
        )
        self.sysStatusPV = PyDMChannel(
            address="ca://{}{}".format(macros["P"], ":OpMode-Sts"),
            value_slot=self.update_sys_state_label,
        )
        self.modStatusPV.connect()
        self.sysStatusPV.connect()

        # Initial reading from epics.PV
        try:
            self.flash_error_history(self.errorHistoryPV.value)
            # self.update_sys_state_labels(self.sysStatusPV.char_value)
            # self.update_mod_state_labels(self.modStatusPV.value)
        except:
            pass

        # --------- Power Up and Operating time ------------
        self.oprTimeChannel = PyDMChannel(
            address="ca://{}{}".format(macros["P"], ":OperatingTime-Mon"),
            value_slot=self.opr_time_update,
        )
        self.pwrupTimeChannel = PyDMChannel(
            address="ca://{}{}".format(macros["P"], ":PowerUpTime-Mon"),
            value_slot=self.prwup_time_update,
        )
        self.operatingTimeDatetime = None
        self.pwrupTimeDatetime = None

        self.oprTimeChannel.connect()
        self.pwrupTimeChannel.connect()

        # ------------ Flash Error History
        # @todo: do this better !
        self.flashHistoryTable.verticalHeader().setVisible(False)

        self.errorHistoryPV = epics.PV(
            pvname="{}{}".format(macros["P"], ":ErrorHistory-Mon"),
            callback=self.flash_error_history,
        )
        # ------------- DOCS ------------
        self.btnErrorsDocs.clicked.connect(
            lambda self: QDesktopServices.openUrl(QUrl.fromLocalFile(ERROR_LIST_PDF))
        )

    def opr_time_update(self, value):
        self.operatingTimeDatetime = datetime.timedelta(seconds=value)
        self.lblOperatingTime.setText(str(self.operatingTimeDatetime))
        self.flash_error_history(value=self.errorHistoryPV.value)

    def prwup_time_update(self, value):
        self.pwrupTimeDatetime = datetime.timedelta(seconds=value)
        self.lblPowerupTime.setText(str(self.operatingTimeDatetime))
        self.flash_error_history(value=self.errorHistoryPV.value)

    ###     self.oprTimeChannel = epics.PV(
    ###         pvname="{}{}".format(macros["P"], ":OperatingTime-Mon"),
    ###         callback=self.opr_time_update,
    ###     )
    ###     self.pwrupTimeChannel = epics.PV(
    ###         pvname="{}{}".format(macros["P"], ":PowerUpTime-Mon"),
    ###         callback=self.prwup_time_update,
    ###     )

    ### def opr_time_update(self, *args, **kwargs):
    ###     value = kwargs["value"]
    ###     self.lblOperatingTime.setText(str(datetime.timedelta(seconds=value)))

    ### def prwup_time_update(self, *args, **kwargs):
    ###     value = kwargs["value"]
    ###     self.lblPowerupTime.setText(str(datetime.timedelta(seconds=value)))
    def get_char_val(self, val):
        char_value = ""
        if val == 2:
            char_value = "POWERUP"
        elif val == 4:
            char_value = "READY"
        elif val == 8:
            char_value = "RUN"
        elif val == 10:
            char_value = "WARN"
        elif val == 12:
            char_value = "ERROR"
        elif val == 15:
            char_value = "STOP"
        return char_value

    def get_style_from_state(self, state):

        color = "white"
        bgColor = "gray"

        if state in ["POWERUP", "READY"]:
            bgColor = "darkGreen"
        elif state == "RUN":
            bgColor = "green"
        elif state == "WARN":
            bgColor = "yellow"
        elif bgColor == "ERROR":
            bgColor = "RED"

        return """color: {}; background-color: {};""".format(color, bgColor)

    def update_mod_state_label(self, val):
        char_value = self.get_char_val(val)
        self.modStatus.setText(char_value)
        self.modStatus.setStyleSheet(self.get_style_from_state(char_value))

    def update_sys_state_label(self, val):
        char_value = self.get_char_val(val)
        self.sysStatus.setText(char_value)
        self.sysStatus.setStyleSheet(self.get_style_from_state(char_value))

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

        self.flashHistoryTable.setRowCount(len(values))
        i = 0
        for value in values:
            n, day, hour, minute, second, milli, group, code = value.split(",")
            eventTimedelta = datetime.timedelta(
                days=float(day),
                hours=float(hour),
                seconds=float(second),
                milliseconds=float(milli),
            )
            self.flashHistoryTable.setItem(i, 0, QTableWidgetItem(n))
            self.flashHistoryTable.setItem(
                i, 1, QTableWidgetItem(str(eventTimedelta)),
            )

            if self.operatingTimeDatetime and self.pwrupTimeDatetime:
                self.flashHistoryTable.setItem(
                    i,
                    2,
                    QTableWidgetItem(
                        str(
                            datetime.datetime.now()
                            - (self.operatingTimeDatetime - eventTimedelta)
                        )
                        + " + timeoffset"
                    ),
                )

            self.flashHistoryTable.setItem(
                i, 3, QTableWidgetItem(self.get_group_string(group))
            )
            self.flashHistoryTable.setItem(
                i, 4, QTableWidgetItem(self.get_code_string(code))
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

    def configWidget(self):
        self.tabWidget.setTabEnabled(TabId.System, False)
        self.sysFrame.setVisible(self.isMaster)
        self.btnSysErr.setVisible(self.isMaster)
        self.btnSysWarn.setVisible(self.isMaster)
        self.btnClear.setVisible(self.isMaster)
        self.btnSave.setVisible(self.isMaster)

        try:
            # This function was introduced in Qt 5.15.
            self.tabWidget.setTabVisible(TabId.System, self.isMaster)
        except:
            pass

        self.sysOutVolt.setVisible(self.isMaster)
        self.sysOutCurr.setVisible(self.isMaster)
        self.sysOutPwr.setVisible(self.isMaster)
        self.sysStatus.setVisible(self.isMaster)

        self.warnByte.channel = "ca://{}{}".format(
            self.macros_dict["P"],
            ":GenWarn-Mon" if self.isMaster else ":ModWarnGroup-Mon",
        )
        self.errorByte.channel = "ca://{}{}".format(
            self.macros_dict["P"],
            ":GenIntlk-Mon" if self.isMaster else ":ModErrGroup-Mon",
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
        if self.isMaster:
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
            self.tabWidget.setTabEnabled(TabId.System, unlock)

        self.tabWidget.setTabEnabled(TabId.Module, unlock)
        self.tabWidget.setTabEnabled(TabId.ErrWarn, unlock)
        self.tabWidget.setTabEnabled(TabId.Advanced, unlock)

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
