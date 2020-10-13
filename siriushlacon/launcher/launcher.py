import json
import os
from qtpy.QtGui import QPixmap
from pydm import Display

from siriushlacon import __version__
from siriushlacon.agilent4uhv.consts import (
    AGILENT_MAIN,
    AGILENT_OVERVIEW,
    AGILENT_EXTENDED,
)
from siriushlacon.agilent4uhv.extended import MainWindow
from siriushlacon.launcher.consts import LAUNCH_WINDOW_UI, PCTRL_MAIN
from siriushlacon.mbtemp.consts import MBTEMP_MAIN
from siriushlacon.mks937b.consts import MKS_MAIN, MKS_OVERVIEW
from siriushlacon.regatron.consts import REGATRON_MAIN
from siriushlacon.spixconv.consts import SPIXCONV_MAIN
from siriushlacon.countingpru.consts import GAMMA_COUNTING_MAIN
from siriushlacon.beaglebones.consts import BEAGLEBONES_MAIN
from siriushlacon.vbc.consts import MAIN_WINDOW_PY as VBC_MAIN_WINDOW_PY
from siriushlacon.utils.consts import (
    CNPEM_INVISIBLE_IMG,
    LNLS_INVISIBLE_IMG,
    BO,
    SI,
    TB,
    TS,
)


class Launcher(Display):
    """
    Vacuum main application interface that gives access to all devices.
    """

    def __init__(self, parent=None, args=[], macros=None, **kwargs):
        super(Launcher, self).__init__(parent=parent, args=args, macros=macros)

        self.lblVersion.setText("v" + __version__)
        self.btnVbc.filenames = [VBC_MAIN_WINDOW_PY]
        self.btnVbc.openInNewWindow = True

        self.btnAgilentExtended.passwordProtected = True
        self.btnAgilentExtended.password = "VACS"
        self.btnAgilentExtended.clicked.connect(self.launchAgilentExtended)

        self.btnAgilent.filenames = [AGILENT_MAIN]
        self.btnAgilent.openInNewWindow = True
        self.btnAgilentSROverview.filenames = [AGILENT_OVERVIEW]
        self.btnAgilentSROverview.macros = json.dumps(
            {
                "device": "UHV",
                "TYPE": SI,
                "TITLE": "ION Pump Agilent 4UHV - SI",
                "FORMAT": "EXP",
            }
        )
        self.btnAgilentSROverview.openInNewWindow = True

        self.btnAgilentBOOverview.filenames = [AGILENT_OVERVIEW]
        self.btnAgilentBOOverview.macros = json.dumps(
            {
                "device": "UHV",
                "TYPE": BO,
                "TITLE": "ION Pump Agilent 4UHV - BO",
                "FORMAT": "EXP",
            }
        )
        self.btnAgilentBOOverview.openInNewWindow = True

        self.btnAgilentTBOverview.filenames = [AGILENT_OVERVIEW]
        self.btnAgilentTBOverview.macros = json.dumps(
            {
                "device": "UHV",
                "TYPE": TB,
                "TITLE": "ION Pump Agilent 4UHV - TB",
                "FORMAT": "EXP",
            }
        )
        self.btnAgilentTBOverview.openInNewWindow = True

        self.btnAgilentTSOverview.filenames = [AGILENT_OVERVIEW]
        self.btnAgilentTSOverview.macros = json.dumps(
            {
                "device": "UHV",
                "TYPE": TS,
                "TITLE": "ION Pump Agilent 4UHV - TS",
                "FORMAT": "EXP",
            }
        )
        self.btnAgilentTSOverview.openInNewWindow = True

        self.btnMks.filenames = [MKS_MAIN]
        self.btnMks.openInNewWindow = True

        self.btnMksSROverview.filenames = [MKS_OVERVIEW]
        self.btnMksSROverview.macros = json.dumps(
            {"device": "MKS", "TYPE": SI, "TITLE": "MKS 937b - SI"}
        )
        self.btnMksSROverview.openInNewWindow = True

        self.btnMksTBOverview.filenames = [MKS_OVERVIEW]
        self.btnMksTBOverview.macros = json.dumps(
            {"device": "MKS", "TYPE": TB, "TITLE": "MKS 937b - TB"}
        )
        self.btnMksTBOverview.openInNewWindow = True

        self.btnMksTSOverview.filenames = [MKS_OVERVIEW]
        self.btnMksTSOverview.macros = json.dumps(
            {"device": "MKS", "TYPE": TS, "TITLE": "MKS 937b - TS"}
        )
        self.btnMksTSOverview.openInNewWindow = True

        self.btnMksBOOverview.filenames = [MKS_OVERVIEW]
        self.btnMksBOOverview.macros = json.dumps(
            {"device": "MKS", "TYPE": BO, "TITLE": "MKS 937b - BO"}
        )
        self.btnMksBOOverview.openInNewWindow = True

        self.btnMBTemp.filenames = [MBTEMP_MAIN]
        self.btnMBTemp.openInNewWindow = True

        self.btnProcServCtrl.filenames = [PCTRL_MAIN]
        self.btnProcServCtrl.openInNewWindow = True

        self.btnRegatron.filenames = [REGATRON_MAIN]
        self.btnRegatron.openInNewWindow = True

        self.btnEpp.filenames = [SPIXCONV_MAIN]
        self.btnEpp.openInNewWindow = True

        self.btnGamma.filenames = [GAMMA_COUNTING_MAIN]
        self.btnGamma.openInNewWindow = True

        self.btnBBB.filenames = [BEAGLEBONES_MAIN]
        self.btnBBB.openInNewWindow = True

        self.btnExit.clicked.connect(self.exitApp)

        self.label_cnpem.setPixmap(QPixmap(CNPEM_INVISIBLE_IMG))
        self.label_lnls.setPixmap(QPixmap(LNLS_INVISIBLE_IMG))

    def launchAgilentExtended(self):
        if self.btnAgilentExtended.validate_password():
            # @fixme: We need a better way to launch this
            self.window = MainWindow()
            self.window.show()

    def exitApp(self):
        exit()

    def ui_filename(self):
        return LAUNCH_WINDOW_UI

    def ui_filepath(self):
        return LAUNCH_WINDOW_UI
