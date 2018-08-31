#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydm import Display
from pydm.utilities import IconFont
from os import path

from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QListWidget, QVBoxLayout,\
                            QPushButton, QFileDialog, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal, QObject

from utils import get_abs_path
from consts import IOC_MAN_UI, IOC_FILENAME
import psutil
import json

from threading import  Thread, Event
from ioc import worker, kill_ioc, get_process

class IocMan(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(IocMan, self).__init__(parent=parent, args=args, macros=macros)

        # self.iocFileName = IOC_FILENAME

        self.vBoxLayout = QVBoxLayout(self.frame_2)
        self.aListWidget = QListWidget()

        self.btnReboot = QPushButton('Reboot IOC')

        self.iocBootDiag = QPushButton('Select iocBoot File') 
        self.iocBootLocal = QLabel(IOC_FILENAME)
        self.iocBootLocal.setAlignment(Qt.AlignHCenter)
        
        self.pKillLog = QLabel()
        self.pKillLog.setAlignment(Qt.AlignHCenter)

        self.vBoxLayout.addWidget(self.aListWidget, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.btnReboot, Qt.AlignHCenter)
 
        self.vBoxLayout.addWidget(self.iocBootDiag, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.iocBootLocal, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.pKillLog, Qt.AlignHCenter)
        
        worker.parse_triggered.connect(self.update_process)

        self.iocBootDiag.clicked.connect(self.getDir)
        self.btnReboot.clicked.connect(self.killProcess)

        self.update_process()

  
    def killProcess(self):
        # print('pKill')
        # log = ''
        # try:
        #     pidToKill = []
        #     process_name = self.iocFileName.split('/')[-1]
        #     print('pName{}'.format(process_name))
        #     for proc in psutil.process_iter():
        #         pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'exe', 'create_time'])

        #         if process_name == pinfo['name'] or  process_name in pinfo['name']:
        #             pidToKill.append(pinfo['pid'])
        #             print(pinfo)

        #     for pid in pidToKill:
        #         parent = psutil.Process(pid)
        #         children = parent.children(recursive=True)

        #         if include_parent:
        #             children.append(parent)

        #         for p in children:
        #             p.terminate()
        #         gone, alive = psutil.wait_procs(children, timeout=3, callback=self.on_terminate)
        #         for p in alive:
        #             p.kill()
                    
        #         parent.kill() 
        # except Exception as e:
        #     print('Excep: {}'.format(e))
        #     log = '{}'.format(e)
        res = kill_ioc()
        if res:
            self.pKillLog.setText(res)
  
    def getDir(self):
        global IOC_FILENAME
        string = QFileDialog.getOpenFileName(self, "Select the iocBoot file.", IOC_FILENAME, "cmd (*.cmd)")
        # print(string)
        try:
            IOC_FILENAME = string[0]
            self.iocBootLocal.setText(IOC_FILENAME)
        except:
            pass

    def update_process(self):
        list = get_process()
        self.aListWidget.clear()
        
        # for proc in psutil.process_iter():
        #     try:
        #         pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'exe', 'create_time'])
        #     except psutil.NoSuchProcess:
        #         pass
        #     else: 
        #         if '.cmd' in pinfo['name'] or 'proc' in pinfo['name']:
        #             list.append(json.dumps(pinfo))

        for i in list:
            lbl = QListWidgetItem()
            lbl.setText(i)
            lbl.setTextAlignment(Qt.AlignHCenter)
            self.aListWidget.addItem(lbl)
                
    def ui_filename(self):
        return IOC_MAN_UI

    def ui_filepath(self):
        return get_abs_path(IOC_MAN_UI)