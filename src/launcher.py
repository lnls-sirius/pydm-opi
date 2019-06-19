from pydm import Display
from pydm import PyDMApplication
import json

from src.paths import LAUNCH_WINDOW_UI, AGILENT_MAIN, MKS_MAIN, MBTEMP_MAIN, OVERVIEW, get_abs_path, MKS_OVERVIEW

class Launcher(Display):
    """
    Vacuum main application interface that gives access to all devices.
    """
    def __init__(self, parent=None, args=[], macros=None, **kwargs):
        super(Launcher, self).__init__(parent=parent, args=args, macros=macros)
        self.btnAgilent.displayFilename = get_abs_path(AGILENT_MAIN)
        self.btnAgilent.openInNewWindow = True

        self.btnAgilentSROverview.displayFilename = get_abs_path(OVERVIEW)
        self.btnAgilentSROverview.base_macros = {"device":"UHV", 'TYPE':'SR', "TITLE": "ION Pump Agilent 4UHV - SI and TS", 'FORMAT': 'EXP'}
        self.btnAgilentSROverview.openInNewWindow = True

        self.btnAgilentBOOverview.displayFilename = get_abs_path(OVERVIEW)
        self.btnAgilentBOOverview.base_macros = {"device":"UHV", 'TYPE':'BO', "TITLE": "ION Pump Agilent 4UHV - BO and TB", 'FORMAT': 'EXP'}
        self.btnAgilentBOOverview.openInNewWindow = True

        self.btnMks.displayFilename = get_abs_path(MKS_MAIN)
        self.btnMks.openInNewWindow = True

        self.btnMksSROverview.displayFilename = get_abs_path(MKS_OVERVIEW)
        self.btnMksSROverview.base_macros = {"device":"MKS", 'TYPE':'SR', "TITLE": "MKS 937b - SI and TS"}
        self.btnMksSROverview.openInNewWindow = True

        self.btnMksBOOverview.displayFilename = get_abs_path(MKS_OVERVIEW)
        self.btnMksBOOverview.base_macros = {"device":"MKS", 'TYPE':'BO', "TITLE": "MKS 937b - BO and TB"}
        self.btnMksBOOverview.openInNewWindow = True

        self.btnMBTemp.displayFilename = get_abs_path(MBTEMP_MAIN)
        self.btnMBTemp.openInNewWindow = True


        self.btnExit.clicked.connect(self.exitApp)

    def exitApp(self):
        exit()

    def ui_filename(self):
        return LAUNCH_WINDOW_UI

    def ui_filepath(self):
        return get_abs_path(LAUNCH_WINDOW_UI)

