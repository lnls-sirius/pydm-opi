#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import psutil
import json
from threading import Thread, Event

from PyQt5.QtCore import Qt, pyqtSignal, QObject

from src.mks937b.consts import IOC_FILENAME


class Worker(QObject):
    parse_triggered = pyqtSignal()

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)


worker = None


def go__():
    global worker
    worker = Worker()
    event = Event()
    while True:
        event.wait(1)
        worker.parse_triggered.emit()


t = Thread(target=go__)
t.setDaemon(True)
t.start()


def get_process():
    list = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(
                attrs=['pid', 'name', 'username', 'exe', 'create_time'])
        except psutil.NoSuchProcess:
            pass
        else:
            if '.cmd' in pinfo['name'] or 'proc' in pinfo['name']:
                list.append(json.dumps(pinfo))
    return list


def on_terminate(proc):
    print("process {} terminated with exit code {}".format(proc, proc.returncode))


def kill_ioc(include_parent=True, callback=on_terminate):
    log = ''
    try:
        pidToKill = []
        process_name = IOC_FILENAME.split('/')[-1]
        for proc in psutil.process_iter():
            pinfo = proc.as_dict(
                attrs=['pid', 'name', 'username', 'exe', 'create_time'])

            if process_name == pinfo['name'] or process_name in pinfo['name']:
                pidToKill.append(pinfo['pid'])
                log += 'Killed {} {} {}'.format(
                    pinfo['pid'], pinfo['name'], pinfo['exe'])
                # print(pinfo)

        for pid in pidToKill:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)

            if include_parent:
                children.append(parent)

            for p in children:
                p.terminate()
            gone, alive = psutil.wait_procs(
                children, timeout=3, callback=callback)
            for p in alive:
                p.kill()
            parent.kill()

    except Exception as e:
        print('Excep: {}'.format(e))
        log = '{}'.format(e)

    if log == '':
        log = 'No process related to {} has been found !'.format(IOC_FILENAME)
    return log
