from pydm import Display
from pydm import PyDMApplication

from PyQt5.QtWidgets import QStyleFactory

from src.paths import LAUNCH_WINDOW_UI, AGILENT_MAIN, MKS_MAIN, MBTEMP_MAIN, get_abs_path

class Launcher(Display):
    """
    Vacuum main application interface that gives access to all devices.
    """
    def __init__(self, parent=None, args=[], macros=None):
        super(Launcher, self).__init__(parent=parent, args=args, macros=macros) 

        self.btnAgilent.displayFilename = get_abs_path(AGILENT_MAIN)    
        self.btnAgilent.openInNewWindow = True 

        self.btnMks.displayFilename = get_abs_path(MKS_MAIN)     
        self.btnMks.openInNewWindow = True

        self.btnMBTemp.displayFilename = get_abs_path(MBTEMP_MAIN)     
        self.btnMBTemp.openInNewWindow = True
        
        self.btnExit.clicked.connect(self.exitApp)

    def exitApp(self):
        exit()

    def ui_filename(self):
        return LAUNCH_WINDOW_UI

    def ui_filepath(self):
        return get_abs_path(LAUNCH_WINDOW_UI)
        