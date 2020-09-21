#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging, requests, sys
from pydm import Display
from pydm.widgets.channel import PyDMChannel
from qtpy import QtWidgets, QtCore
from qtpy.QtGui import QPixmap
from functools import partial

from siriushlacon.mbtemp.consts import (
    MBTEMP_MAIN,
    MBTEMP_MAIN_UI,
    OVERVIEW_MAIN,
    BOEXTRACTION_PIC,
    OVERVIEW_MAIN,
    BOINJ_PIC,
    BO_PIC1,
    BO_PIC2,
    BO_PIC3,
    BO_PIC4,
    SR_PICS,
    CNPEM_LOGO,
    LNLS_LOGO,
    SRINJ_PIC,
    PIC_P7RF,
    SR_PICS,
    PIC_PA,
    PIC_LA,
)

logger = logging.getLogger()

TAB = {0: "RF", 1: "TB", 2: "TS", 3: "BO", 4: "SI", 5: "LA", 6: "PA"}

DEVICES_IP = {  # {Area IPs:[ip, devices (To specific devices only)]}
    "RF": [["10.128.102.119", [None, None]], ["10.128.101.118", [None, None]]],
    "TB": [["10.128.119.106", [5, 6]]],
    "TS": [["10.128.120.106", [0, 4]], ["10.128.101.117", [3, 4]]],
    "LA": [["10.128.122.102", [None, None]]],
    "PA": [["10.128.123.131", [None, None]], ["10.128.123.132", [None, None]]],
    "BO": [["10.128.1{:0>2d}.106", [None, None]]],
    "SI": [
        ["10.128.1{:0>2d}.117", [None, None]],
        ["10.128.1{:0>2d}.118", [None, None]],
    ],
}


class MBTempMonitoring(Display):
    def __init__(self, parent=None, macros=None, args=None):
        super().__init__(
            parent=parent, args=args, macros=macros, ui_filename=MBTEMP_MAIN_UI
        )
        self.OverviewButton.filenames = [OVERVIEW_MAIN]
        self.OverviewButton.openInNewWindow = True

        self.tab = ""
        self.addr = []
        self.url = "http://10.0.38.42:26001/devices"

        self.P7RF.setPixmap(QPixmap(PIC_P7RF))
        self.BOInj.setPixmap(QPixmap(BOINJ_PIC))
        self.SRInj.setPixmap(QPixmap(SRINJ_PIC))
        self.LinacArea.setPixmap(QPixmap(PIC_LA))
        self.PowerArea.setPixmap(QPixmap(PIC_PA))
        self.LogoLNLS.setPixmap(QPixmap(LNLS_LOGO))
        self.LogoCNPEM.setPixmap(QPixmap(CNPEM_LOGO))
        self.BOExtraction.setPixmap(QPixmap(BOEXTRACTION_PIC))

        for SRimg in range(1, 8):
            getattr(self, "SR_Pic{}".format(SRimg)).setPixmap(QPixmap(SR_PICS[SRimg]))

        self.tabWidget.currentChanged.connect(self.sector_change_connect)
        self.sector.valueChanged.connect(self.sector_change_connect)

        self.sector_change_connect()

    def sector_change_connect(self):
        self.tab = TAB[self.tabWidget.currentIndex()]
        self.sector_change_disconnect()

        channels = []
        self.board_sensors = {}

        logger.info("Area {}; Sector {}".format(self.tab, self.sector.value()))

        try:
            info_request = requests.get(
                self.url, verify=False, params={"type": "mbtemp"}, timeout=5
            )
        except:
            QtWidgets.QMessageBox.warning(
                self, "Warning", "Impossible connect to {}".format(self.url)
            )
            logger.warning("Impossible connect to {}".format(self.url))
            sys.exit()
        dev = info_request.json()

        if self.tab in ["RF", "TB", "TS", "LA", "PA"]:
            self.sector.setEnabled(False)

        elif self.tab == "BO":
            self.sector.setSingleStep(2)
            self.sector.setEnabled(True)
            self.sector.setMaximum(19)

            if self.sector.value() % 2 == 0:
                self.sector.setValue(1)

            sectorFrom = 2 + (self.sector.value() // 2) * 5
            sectorTo = 7 + (self.sector.value() // 2) * 5

            for x, y in enumerate(range(sectorFrom, sectorTo)):
                if y != 51:
                    getattr(self, "BO_Sec_{}".format(x + 1)).setText(
                        "Booster Sector: {}".format(y)
                    )
                else:
                    self.BO_Sec_5.setText("Booster Sector: 1")
            self.setBOImage(sectorFrom)
        else:
            self.sector.setSingleStep(1)
            self.sector.setEnabled(True)
            self.sector.setMaximum(20)

        for ip in DEVICES_IP[self.tab]:  # dict -> {MBTemp:[CH1,CH2...]}
            for board in dev[ip[0].format(self.sector.value())][ip[1][0] : ip[1][1]]:
                for enabled in range(1, 9):
                    channels.append(board["channels"]["CH{}".format(enabled)]["prefix"])
                self.board_sensors[board["prefix"]] = channels
                channels = []

        for mbtemp in self.board_sensors:
            for coef in ["Alpha", "LinearCoef-Mon", "AngularCoef-Mon"]:
                slot = partial(
                    self.update_mbtemp,
                    pvname=mbtemp,
                    coef=coef,
                    sector=self.sector.value(),
                )
                mb = PyDMChannel(
                    address="ca://{}:{}".format(mbtemp, coef),
                    value_slot=slot,
                    connection_slot=slot,
                )
                self.addr.append(mb)
                mb.connect()

            for number, pv in enumerate(self.board_sensors[mbtemp]):
                slot = partial(
                    self.update_channel,
                    name_pv=pv,
                    mbtemp_name=mbtemp,
                    mbtemp_ch=number + 1,
                )
                temp = PyDMChannel(
                    address="ca://" + pv, value_slot=slot, connection_slot=slot
                )
                self.addr.append(temp)
                temp.connect()

    def update_channel(self, value, name_pv, mbtemp_name, mbtemp_ch):

        chosenArea = self.tab
        _id = mbtemp_name[-2:]

        try:
            if chosenArea == "TS":
                if _id == "14":
                    chosenArea = "SI"
                aux = _id

            elif chosenArea == "BO" and mbtemp_ch < 4 and mbtemp_name != "TB-MBTemp":
                location = int(_id) % 5
                aux = location if location != 0 else 5

            elif chosenArea in ["SI", "PA", "LA"]:
                aux = _id
                if (mbtemp_ch == 3) and (
                    mbtemp_name in ["SI-01-MBTemp-13", "SI-20-MBTemp-23"]
                ):
                    aux += "_2"

            elif chosenArea == "RF":
                aux = _id
                if _id == "23":
                    aux += "_2"
                    chosenArea = "SI"

            elif chosenArea == "TB":
                if mbtemp_name[:-3] == "BO-MBTemp":
                    return ()
                aux = ""

            else:
                return ()
            channel = getattr(self, "{}{}_Ch{}".format(chosenArea, aux, mbtemp_ch))

        except AttributeError or ValueError:
            return ()

        # ----------- Update color and toolTip ----------
        if value == False or value < 1:
            channel.brush = QtCore.Qt.red
            channel.setToolTip(
                ("PV: {}\n" + "Channel: {}\n" + "Process Variable Disconnected").format(
                    name_pv, mbtemp_ch
                )
            )
            return ()
        elif value == True:
            channel.brush = QtCore.Qt.green
            return ()
        elif value > self.tempMax.value():
            if (value > 410) and (value < 425):
                channel.brush = QtCore.Qt.cyan
                channel.setToolTip(
                    ("PV: {}\n" + "The Channel {} of MBTemp {} is open!").format(
                        name_pv, mbtemp_ch, mbtemp_name
                    )
                )
                return ()
            else:
                channel.brush = QtCore.Qt.yellow
        else:
            channel.brush = QtCore.Qt.green

        channel.setToolTip(
            (
                "Temperature: {} °C\n" + "MBTemp: {}\n" + "Channel: {}\n" + "PV: {}"
            ).format(value, mbtemp_name, mbtemp_ch, name_pv)
        )

    def update_mbtemp(self, value, pvname, coef, sector):
        last_Value = []
        new_val = {"Alpha": 0, "Linear Coefficient": "", "Angular Coefficient": ""}
        coefficients = {
            "Alpha": "Alpha",
            "LinearCoef-Mon": "Linear Coefficient",
            "AngularCoef-Mon": "Angular Coefficient",
        }

        try:
            id_addr = int(pvname[-2:])
        except:
            if self.tab != "TB":
                return ()
            else:
                mb = 1

        if self.tab == "BO":
            location = id_addr % 5
            mb = location if location != 0 else 5

        elif self.tab in ["TS", "SI", "PA", "LA", "RF"]:
            mb = id_addr
        try:
            mbtemp = getattr(self, "{}_MBTemp{:0>2d}".format(self.tab, mb))
        except AttributeError:
            return ()

        if value == False:
            mbtemp.brush = QtCore.Qt.red
            mbtemp.setToolTip(("{} - MBTemp Board is disconnected").format(pvname))
            return ()
        elif value == True:
            mbtemp.brush = QtCore.Qt.blue
            return ()
        mbtemp.brush = QtCore.Qt.blue

        last_Value = mbtemp.toolTip().split("\n")

        for val in last_Value[1:]:
            new_val[val.split(": ")[0]] = val.split(": ")[1]

        new_val[coefficients[coef]] = value

        mbtemp.setToolTip(
            (
                "MBTemp: {}\n"
                + "Alpha: {}\n"
                + "Linear Coefficient: {}\n"
                + "Angular Coefficient: {}"
            ).format(
                pvname,
                new_val["Alpha"],
                new_val["Linear Coefficient"],
                new_val["Angular Coefficient"],
            )
        )

    def sector_change_disconnect(self):
        for channel in self.addr:
            channel.disconnect()
        if self.tab != "SI":
            return ()

        for disc in [
            "11_Ch4",
            "11_Ch5",
            "11_Ch6",
            "13_Ch8",
            "22_Ch6",
            "13_Ch3",
            "10_Ch1",
            "10_Ch2",
            "23_Ch8",
            "11_Ch2",
            "21_Ch1",
            "22_Ch4",
            "23_Ch3",
            "23_2_Ch3",
            "23_Ch4",
            "13_2_Ch3",
            "_MBTemp10",
        ]:
            getattr(self, "SI{}".format(disc)).brush = QtCore.Qt.gray
            getattr(self, "SI{}".format(disc)).setToolTip("")

    def setBOImage(self, secFrom):
        if secFrom % 2 == 0:
            self.BO_Img1.setPixmap(QPixmap(BO_PIC3))
            self.BO_Img2.setPixmap(QPixmap(BO_PIC2))
            self.BO_Img3.setPixmap(QPixmap(BO_PIC3))
            self.BO_Img4.setPixmap(QPixmap(BO_PIC1))
            self.BO_Img5.setPixmap(QPixmap(BO_PIC3))
        else:
            self.BO_Img1.setPixmap(QPixmap(BO_PIC1))
            self.BO_Img2.setPixmap(QPixmap(BO_PIC4))
            self.BO_Img3.setPixmap(QPixmap(BO_PIC1))
            self.BO_Img4.setPixmap(QPixmap(BO_PIC3))
            self.BO_Img5.setPixmap(QPixmap(BO_PIC1))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MBTempMonitoring()
    window.show()
    sys.exit(app.exec_())
