#!/usr/bin/env python3
import json
import logging

from pydm import Display
from pydm.widgets.related_display_button import PyDMRelatedDisplayButton
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QGridLayout

from siriushlacon.regatron.consts import REGATRON_UI, DATA_JSON, COMPLETE_MAIN
from siriushlacon.utils.consts import CNPEM_IMG, LNLS_IMG

logger = logging.getLogger()


def load_data():
    data = None
    with open(DATA_JSON, "rb") as f:
        data = json.load(f)
    return data


def get_overview_detail(data):
    name = data["P"]
    overview = PyDMRelatedDisplayButton(name)
    overview.macros = [json.dumps(data)]
    overview.filenames = [COMPLETE_MAIN]
    overview.openInNewWindow = True
    overview.showIcon = False
    return overview


class Launcher(Display):
    DIP = "DIP"
    QUA = "QUA"
    SEX = "SEX"

    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, ui_filename=REGATRON_UI)
        self.logo_cnpem.setPixmap(QPixmap(CNPEM_IMG))
        self.logo_lnls.setPixmap(QPixmap(LNLS_IMG))

        self.data = load_data()
        self.layoutDipoles = QGridLayout()
        self.layoutQuadrupoles = QGridLayout()
        self.layoutSextupoles = QGridLayout()

        self.tabDipoles.setLayout(self.layoutDipoles)
        self.tabQuadrupoles.setLayout(self.layoutQuadrupoles)
        self.tabSextupoles.setLayout(self.layoutSextupoles)

        self.dipole = []
        self.quadrupole = []
        self.sextupole = []

        for e in self.data:
            if e["type"] == self.QUA:
                self.quadrupole.append(e)
            elif e["type"] == self.DIP:
                self.dipole.append(e)
            elif e["type"] == self.SEX:
                self.sextupole.append(e)

        self.render(self.layoutDipoles, self.dipole)
        self.render(self.layoutQuadrupoles, self.quadrupole)
        self.render(self.layoutSextupoles, self.sextupole)

    def render(self, layout, data):
        i = 0
        for name in data:
            overview = get_overview_detail(name)
            layout.addWidget(overview, i, 0)
            i += 1
        layout.setRowStretch(len(data), 10)
