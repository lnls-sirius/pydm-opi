import subprocess

from qtpy.QtGui import QPixmap

from pydm import Display

from siriushlacon.agilent4uhv.consts import AGILENT_MAIN, AGILENT_OVERVIEW
from siriushlacon.mbtemp.consts import MBTEMP_MAIN
from siriushlacon.mks937b.consts import MKS_MAIN, MKS_OVERVIEW
from siriushlacon.regatron.consts import REGATRON_MAIN
from siriushlacon.launcher.consts import LAUNCH_WINDOW_UI, PCTRL_MAIN
from siriushlacon.spixconv.consts import SPIXCONV_MAIN
from siriushlacon.utils.consts import CNPEM_IMG, LNLS_IMG

class Launcher(Display):
    """
    Vacuum main application interface that gives access to all devices.
    """
    def __init__(self, parent=None, args=[], macros=None, **kwargs):
        super(Launcher, self).__init__(parent=parent, args=args, macros=macros)
        self.btnAgilent.filenames = [AGILENT_MAIN]
        self.btnAgilent.openInNewWindow = True

        self.btnAgilentSROverview.filenames = [AGILENT_OVERVIEW]
        self.btnAgilentSROverview.base_macros = {
            "device": "UHV",
            "TYPE": "SR",
            "TITLE": "ION Pump Agilent 4UHV - SI and TS",
            "FORMAT": "EXP"}
        self.btnAgilentSROverview.openInNewWindow = True

        self.btnAgilentBOOverview.filenames = [AGILENT_OVERVIEW]
        self.btnAgilentBOOverview.base_macros = {
            "device": "UHV",
            "TYPE": "BO",
            "TITLE": "ION Pump Agilent 4UHV - BO and TB",
            "FORMAT": "EXP"}
        self.btnAgilentBOOverview.openInNewWindow = True

        self.btnMks.filenames = [MKS_MAIN]
        self.btnMks.openInNewWindow = True

        self.btnMksSROverview.filenames = [MKS_OVERVIEW]
        self.btnMksSROverview.base_macros = {
            "device": "MKS",
            "TYPE": "SR",
            "TITLE": "MKS 937b - SI and TS"}
        self.btnMksSROverview.openInNewWindow = True

        self.btnMksBOOverview.filenames = [MKS_OVERVIEW]
        self.btnMksBOOverview.base_macros = {
            "device": "MKS",
            "TYPE": "BO",
            "TITLE": "MKS 937b - BO and TB"}
        self.btnMksBOOverview.openInNewWindow = True

        self.btnMBTemp.filenames = [MBTEMP_MAIN]
        self.btnMBTemp.openInNewWindow = True

        self.btnProcServCtrl.filenames = [PCTRL_MAIN]
        self.btnProcServCtrl.openInNewWindow = True

        self.btnRegatron.filenames = [REGATRON_MAIN]
        self.btnRegatron.openInNewWindow = True

        self.btnEpp.filenames = [SPIXCONV_MAIN]
        self.btnEpp.openInNewWindow = True

        self.btnExit.clicked.connect(self.exitApp)

        self.label_cnpem.setPixmap(QPixmap(CNPEM_IMG))
        self.label_lnls.setPixmap(QPixmap(LNLS_IMG))

    def exitApp(self):
        exit()

    def ui_filename(self):
        return LAUNCH_WINDOW_UI

    def ui_filepath(self):
        return LAUNCH_WINDOW_UI
