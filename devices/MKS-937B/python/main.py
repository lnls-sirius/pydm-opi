#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydm import Display
from os import path

from utils import get_abs_path
from consts import MAIN_UI, STORAGE_RING_PY, BOOSTER_PY, BTS_PY, LTB_PY, IOC_MAN_PY
from pydm.utilities import IconFont
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

from ioc import kill_ioc

class Main(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(Main, self).__init__(parent=parent, args=args, macros=macros)
        
        self.btnRing.displayFilename = get_abs_path(get_abs_path(STORAGE_RING_PY)) 
        self.btnRing.setIcon(IconFont().icon('circle'))
        
        self.btnBooster.displayFilename = get_abs_path(get_abs_path(BOOSTER_PY)) 
        self.btnBooster.setIcon(IconFont().icon('forward'))
                
        self.btnBts.displayFilename = get_abs_path(get_abs_path(BTS_PY)) 
        self.btnBts.setIcon(IconFont().icon('arrow-right'))

        self.btnLtb.displayFilename = get_abs_path(get_abs_path(LTB_PY)) 
        self.btnLtb.setIcon(IconFont().icon('arrow-right'))
        
        self.btnIocMan.displayFilename = get_abs_path(get_abs_path(IOC_MAN_PY)) 
        self.btnIocMan.setIcon(IconFont().icon('arrow-right'))
        
        self.btnIocReboot.clicked.connect(self.reboot_ioc)
        self.btnIocReboot.setIcon(IconFont().icon('arrow-right'))
    
    def clear_text(self):
        self.lbl_reboot.setText('')

    def reboot_ioc(self):
        reply = QMessageBox.question(self, "Do you really wish to reboot the IOC?", "Reboot IOC ?", QMessageBox.Yes, QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            res = kill_ioc()
        else:
            res = 'Operation aborted !'
        self.lbl_reboot.setText(res)
        QTimer.singleShot(3000, self.clear_text)


    def ui_filename(self):
        return MAIN_UI

    def ui_filepath(self):
        return get_abs_path(MAIN_UI)