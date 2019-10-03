from pydm import Display

import subprocess
from src.launcher.consts import LAUNCH_WINDOW_UI
from src.agilent4uhv.consts import AGILENT_MAIN, AGILENT_OVERVIEW
from src.mbtemp.consts import MBTEMP_MAIN
from src.mks937b.consts import MKS_MAIN, MKS_OVERVIEW
from src.launcher.consts import PCTRL_MAIN


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

        self.btnEpp.clicked.connect(self.launch_epp)
        self.btnRegatron.clicked.connect(self.launch_regatron)

        self.btnExit.clicked.connect(self.exitApp)

    def launch_epp(self):
        subprocess.Popen(
            'cd ../SPIxCONV/software/pydm/launcher; '
            'pydm --hide-nav-bar launch_ui_main_window.py',
            shell=True)

    def launch_regatron(self):
        subprocess.Popen(
            'cd ../cons-topcon/opi; '
            'pydm --hide-nav-bar launch.py',
            shell=True)

    def exitApp(self):
        exit()

    def ui_filename(self):
        return LAUNCH_WINDOW_UI

    def ui_filepath(self):
        return LAUNCH_WINDOW_UI
