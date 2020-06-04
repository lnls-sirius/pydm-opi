#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from pydm import Display
from pydm.widgets.channel import PyDMChannel
from qtpy import QtWidgets, QtCore
from qtpy.QtGui import QPixmap

from openpyxl import load_workbook

from functools import partial

from siriushlacon.mbtemp.consts import (
    CHS_MBTEMP,
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
    SR_PICS,
    PIC_PA,
    PIC_LA,
)

logger = logging.getLogger()

TAB = {0: "TB", 1: "TS", 2: "BO", 3: "SR", 4: "LA", 5: "PA"}


class MBTempMonitoring(Display):
    def __init__(self, parent=None, macros=None, args=None):
        super().__init__(
            parent=parent, args=args, macros=macros, ui_filename=MBTEMP_MAIN_UI
        )
        self.OverviewButton.filenames = [OVERVIEW_MAIN]
        self.OverviewButton.openInNewWindow = True

        self.tab = ""
        self.addr = []
        self.mbtempID = {}

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

        logger.info("Area {}; Sector {}".format(self.tab, self.sector.value()))

        if self.tab == "TB":
            self.sector.setEnabled(False)
            self.mbtemp = ["TB-MBTemp"]
            self.sensor = ["TB-04:VA-PT100-ED1:Temp-Mon", "TB-04:VA-PT100-ED2:Temp-Mon"]

        elif self.tab == "LA":
            self.sector.setEnabled(False)
            self.mbtemp = ["LA-MBTemp-01", "LA-MBTemp-02", "LA-MBTemp-03"]
            self.sensor = [
                "LA-{:0>2d}PT100-Top:Temp-Mon".format(i) for i in range(1, 5)
            ]
            self.sensor.extend(
                ["LA-{:0>2d}PT100-Down:Temp-Mon".format(i) for i in range(1, 5)]
            )

        elif self.tab == "TS":
            self.sector.setEnabled(False)
            self.mbtemp = ["TS-MBTemp-01", "TS-MBTemp-02"]
            self.sensor = [
                "TS-01:VA-PT100-BG{}:Temp-Mon".format(str(i)) for i in range(1, 5)
            ]
            self.sensor.extend(
                ["TS-04:VA-PT100-ED{}:Temp-Mon".format(str(i)) for i in range(1, 7)]
            )

        elif self.tab == "PA":
            self.sector.setEnabled(False)
            self.mbtemp = ["PA-MBTemp-01", "PA-MBTemp-02", "PA-MBTemp-03"]
            self.sensor = [
                "PA-MBTemp-01:CO-PT100-Ch{}:Temp-Mon".format(str(i))
                for i in range(1, 4)
            ]
            self.sensor.extend(
                [
                    "PA-MBTemp-02:CO-PT100-Ch{}:Temp-Mon".format(str(i))
                    for i in range(1, 4)
                ]
            )
            self.sensor.extend(
                [
                    "PA-MBTemp-03:CO-PT100-Ch{}:Temp-Mon".format(str(i))
                    for i in range(1, 4)
                ]
            )

        elif self.tab == "BO":
            self.sector.setSingleStep(2)
            self.sector.setEnabled(True)
            self.sector.setMaximum(19)

            if self.sector.value() % 2 == 0:
                self.sector.setValue(1)

            sectorFrom = 2 + (self.sector.value() // 2) * 5
            sectorTo = 7 + (self.sector.value() // 2) * 5

            self.setImage(sectorFrom)
            self.mbtemp = [
                "BO-MBTemp-{:0>2d}".format(i)
                for i in range(sectorFrom - 1, sectorTo - 1)
            ]

            for x, y in enumerate(range(sectorFrom, sectorTo)):
                if y != 51:
                    getattr(self, "BO_Sec_{}".format(x + 1)).setText(
                        "Booster Sector: {}".format(y)
                    )
                else:
                    self.BO_Sec_5.setText("Booster Sector: 1")

            if self.sector.value() != 19:
                self.sensor = [
                    "BO-{:0>2d}U:VA-PT100-BG:Temp-Mon".format(i)
                    for i in range(sectorFrom, sectorTo)
                ]
                self.sensor.extend(
                    [
                        "BO-{:0>2d}U:VA-PT100-MD:Temp-Mon".format(i)
                        for i in range(sectorFrom, sectorTo)
                    ]
                )
                self.sensor.extend(
                    [
                        "BO-{:0>2d}U:VA-PT100-ED:Temp-Mon".format(i)
                        for i in range(sectorFrom, sectorTo)
                    ]
                )
            else:
                self.sensor = [
                    "BO-{:0>2d}U:VA-PT100-BG:Temp-Mon".format(i)
                    for i in range(sectorFrom, sectorTo - 1)
                ]
                self.sensor.extend(
                    [
                        "BO-{:0>2d}U:VA-PT100-MD:Temp-Mon".format(i)
                        for i in range(sectorFrom, sectorTo - 1)
                    ]
                )
                self.sensor.extend(
                    [
                        "BO-{:0>2d}U:VA-PT100-ED:Temp-Mon".format(i)
                        for i in range(sectorFrom, sectorTo - 1)
                    ]
                )
                self.sensor.extend(
                    [
                        "BO-01U:VA-PT100-BG:Temp-Mon",
                        "BO-01U:VA-PT100-MD:Temp-Mon",
                        "BO-01U:VA-PT100-ED:Temp-Mon",
                    ]
                )

        elif self.tab == "SR":
            self.sector.setSingleStep(1)
            self.sector.setEnabled(True)
            self.sector.setMaximum(20)

            self.readTable()

        for channel in self.sensor:
            slot = partial(
                self.update_channel, pydmbyte=channel, sector=self.sector.value()
            )
            temp = PyDMChannel(
                address="ca://" + channel, value_slot=slot, connection_slot=slot
            )
            self.addr.append(temp)
            temp.connect()

        for mbtemp in self.mbtemp:
            for coef in ["Alpha", "LinearCoef-Mon", "AngularCoef-Mon"]:
                slot = partial(
                    self.update_mbtemp,
                    pydmbyte=mbtemp,
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

    def update_channel(self, value, pydmbyte, sector):
        # aux = [AddressMBTempBO/SectorOfSR, Pt100PositionOnVaccumChamber, SectorBO/AddressMBTempSR, sectorNumber]
        #                                            [BG, MD, ED, ...]

        if self.tab in ["TS", "TB"]:
            aux = [pydmbyte[3:5], pydmbyte[-10:-9], pydmbyte[3:5], ""]
        elif self.tab == "PA":
            aux = [pydmbyte[10:12], pydmbyte[-10:-9], pydmbyte[10:12], ""]
        elif self.tab == "LA":
            aux = [
                pydmbyte[3:5],
                pydmbyte[11 : pydmbyte.find(":")],
                "{:0>2d}".format(1 + int(pydmbyte[3:5]) // 2),
                "",
            ]

        elif self.tab == "BO":
            if pydmbyte[3:5] != "01":
                aux = [
                    str(int(pydmbyte[3:5]) - (sector // 2) * 5 - 1),
                    pydmbyte[-11:-9],
                    int(pydmbyte[3:5]) - 1,
                    "",
                ]
            else:
                aux = ["5", pydmbyte[-11:-9], "50", ""]

        elif self.tab == "SR":
            _id = self.mbtempID[pydmbyte]
            # print(pydmbyte)
            if not (pydmbyte[5 : pydmbyte.find(":")] in ["SBFE", "SAFE", "SPFE"]):
                if pydmbyte[5 : pydmbyte.find(":")] != "SA":
                    aux = [
                        pydmbyte[5 : pydmbyte.find(":")],
                        pydmbyte[pydmbyte.find("-", 15) + 1 : pydmbyte.find(":", 12)],
                        _id,
                        "-{:0>2d}".format(self.sector.value()),
                    ]
                else:
                    aux = [
                        "SP",
                        pydmbyte[
                            pydmbyte.find("-", 14) + 1 : pydmbyte.find("-", 14) + 3
                        ],
                        _id,
                        "-{:0>2d}".format(self.sector.value()),
                    ]
            else:
                aux = [
                    "FE",
                    pydmbyte[pydmbyte.find("-", 14) + 1 : pydmbyte.find(":", 10)],
                    _id,
                    "-{:0>2d}".format(self.sector.value()),
                ]

        channel = getattr(self, "{}{}_Ch{}".format(self.tab, aux[0], aux[1]))

        # ----------- Update color and toolTip ----------
        if value == False or value < 1:
            channel.brush = QtCore.Qt.red
            return ()
        elif value == True:
            channel.brush = QtCore.Qt.green
            return ()
        elif value > self.tempMax.value():
            channel.brush = QtCore.Qt.yellow
        else:
            channel.brush = QtCore.Qt.green

        channel.setToolTip(
            ("Temperature: {} ºC\n" + "MBTemp: {}\n" + "PV: {}").format(
                value, "{}{}-MBTemp-{}".format(self.tab, aux[3], aux[2]), pydmbyte
            )
        )

    def update_mbtemp(self, value, pydmbyte, coef, sector):
        last_Value = []
        new_val = {"Alpha": 0, "Linear Coefficient": "", "Angular Coefficient": ""}
        coefficients = {
            "Alpha": "Alpha",
            "LinearCoef-Mon": "Linear Coefficient",
            "AngularCoef-Mon": "Angular Coefficient",
        }

        if self.tab == "BO":
            mb = int(pydmbyte[-2:]) - (sector // 2) * 5
        elif self.tab == "TB":
            mb = 1
        elif self.tab in ["TS", "SR", "PA", "LA"]:
            mb = int(pydmbyte[-2:])

        mbtemp = getattr(self, "{}_MBTemp{:0>2d}".format(self.tab, mb))
        if value == False:
            mbtemp.brush = QtCore.Qt.red
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
                "MBTemp:{}\n"
                + "Alpha: {}\n"
                + "Linear Coefficient: {}\n"
                + "Angular Coefficient: {}"
            ).format(
                pydmbyte,
                new_val["Alpha"],
                new_val["Linear Coefficient"],
                new_val["Angular Coefficient"],
            )
        )

    def sector_change_disconnect(self):
        for channel in self.addr:
            channel.disconnect()
        if self.tab != "SR":
            return ()

        for disc in [
            "B2FE_ChBG1",
            "B2FE_ChBG2",
            "B2FE_ChED",
            "B2FE_ChED2",
            "C2_ChBG",
            "BC_ChMD",
            "VPSB1B_ChBG",
        ]:
            getattr(self, "SR{}".format(disc)).brush = QtCore.Qt.gray
            getattr(self, "SR{}".format(disc)).setToolTip("")

    def setImage(self, secFrom):
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

    def readTable(self):
        self.sensor = []
        self.mbtempID = {}
        self.mbtemp = [
            "SI-{:0>2d}-MBTemp-{}".format(self.sector.value(), k)
            for k in [11, 12, 13, 21, 22, 23]
        ]

        wb = load_workbook(filename=CHS_MBTEMP)
        sheet_ranges = wb["Sector{}".format(self.sector.value())]

        for column in ["A", "B", "C", "D", "E", "F"]:
            for line in range(1, 9):
                if (sheet_ranges[column + str(line)].value) != None:
                    self.sensor.append(sheet_ranges[column + str(line)].value)
                    self.mbtempID[
                        sheet_ranges[column + str(line)].value
                    ] = sheet_ranges[column + "10"].value


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MBTempMonitoring()
    window.show()
    sys.exit(app.exec_())
