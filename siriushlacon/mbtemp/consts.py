#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas
import pkg_resources
import os
import urllib.request
import logging
from siriushlacon.utils.consts import get_abs_path as consts_get_abs_path

logger = logging.getLogger()


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


MBTEMP_MAIN = get_abs_path("main.py")
MBTEMP_MAIN_UI = get_abs_path("ui/main.ui")


class Devices:
    _get = None
    _FILE = consts_get_abs_path("Redes e Beaglebones.xlsx")

    @staticmethod
    def load():
        url = "http://10.0.38.42/streamdevice-ioc/Redes%20e%20Beaglebones.xlsx"
        try:
            if not os.access(os.path.dirname(Devices._FILE), os.W_OK):
                Devices._FILE = "/tmp/Redes e Beaglebones.xlsx"

            urllib.request.urlretrieve(url, Devices._FILE)
            logger.info("File {} updated.".format(Devices._FILE))
        except Exception:
            logger.exception(
                "Failed to update the spreadsheet from http://10.0.38.42/streamdevice-ioc/Redes%20e%20Beaglebones.xlsx ! Using old data ..."
            )

    def get(self):
        if not self._get:
            self.load()
            # Devices
            SHEET = "PVs MBTemp"
            sheet = pandas.read_excel(Devices._FILE, sheet_name=SHEET, dtype=str)
            sheet = sheet.replace("nan", "")
            devices = []
            # IP	Rack	ADDR	Dev	CH1	CH2	CH3	CH4	CH5	CH6	CH7	CH8
            for index, row in sheet.iterrows():
                data = [
                    row["Dev"],
                    row["CH1"],
                    row["CH2"],
                    row["CH3"],
                    row["CH4"],
                    row["CH5"],
                    row["CH6"],
                    row["CH7"],
                    row["CH8"],
                ]
                devices.append(data)
            _get = devices
        return _get


devices = Devices()
