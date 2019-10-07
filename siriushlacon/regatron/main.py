#!/usr/bin/python3
import json
import pkg_resources

from pydm import Display
from pydm.widgets.related_display_button import PyDMRelatedDisplayButton
from pydm.widgets.label import PyDMLabel

from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from qtpy.QtGui import QFont

from siriushlacon.regatron.consts import REGATRON_UI, DETAILS_MAIN, SIMPLE_MAIN, DETAILS_MAIN
from siriushlacon.utils.consts import CNPEM_IMG, LNLS_IMG


def load_data():
    data = None
    with pkg_resources.resource_stream(__name__, 'data.json') as f:
        data = json.load(f)
    return data

def get_overview_detail(name):
    overview = PyDMRelatedDisplayButton('Overview')
    overview.macros = ['{"P":"' + name + '"}']
    overview.filenames = [SIMPLE_MAIN]
    overview.openInNewWindow = True
    overview.showIcon = False

    detail = PyDMRelatedDisplayButton('Details')
    detail.macros = ['{"P":"' + name + '"}']
    detail.filenames = [DETAILS_MAIN]
    detail.openInNewWindow = True
    detail.showIcon = False

    return overview, detail


class Launcher(Display):
    DIP = 'DIP'
    QUA = 'QUA'
    SEX = 'SEX'

    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, ui_filename=REGATRON_UI)

        self.label_cnpem.setPixmap(QPixmap(CNPEM_IMG))
        self.label_lnls.setPixmap(QPixmap(LNLS_IMG))

        self.data = load_data()
        self.grid_layout = QGridLayout()
        self.scrollAreaWidgetContents.setLayout(self.grid_layout)

        self.dipole = []
        self.quadrupole = []
        self.sextupole = []

        for e in self.data:
            if e['type'] == self.QUA:
                self.quadrupole.append(e['pv'])
            elif e['type'] == self.DIP: 
                self.dipole.append(e['pv'])
            elif e['type'] == self.SEX:
                self.sextupole.append(e['pv'])
        self.render()

    def render(self):
        category_font = QFont()
        category_font.setBold(True)

        i = 0
        lbl = QLabel('Dipoles')
        lbl.setFont(category_font)
        self.grid_layout.addWidget(lbl, i, 0)
        i += 1

        for name in self.dipole:
            overview, detail  = get_overview_detail(name)

            self.grid_layout.addWidget(QLabel(name), i, 0)
            self.grid_layout.addWidget(overview, i, 1)
            self.grid_layout.addWidget(detail, i, 2)
            i += 1

        lbl = QLabel('Quadrupoles')
        lbl.setFont(category_font)
        self.grid_layout.addWidget(lbl, i, 0)
        i += 1
        for name in self.quadrupole:
            overview, detail  = get_overview_detail(name)

            self.grid_layout.addWidget(QLabel(name), i, 0)
            self.grid_layout.addWidget(overview, i, 1)
            self.grid_layout.addWidget(detail, i, 2)
            i += 1

        lbl = QLabel('Sextupoles')
        lbl.setFont(category_font)
        self.grid_layout.addWidget(lbl, i, 0)
        i += 1
        for name in self.sextupole:
            overview, detail  = get_overview_detail(name)

            self.grid_layout.addWidget(QLabel(name), i, 0)
            self.grid_layout.addWidget(overview, i, 1)
            self.grid_layout.addWidget(detail, i, 2)
            i += 1