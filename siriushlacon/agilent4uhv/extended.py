#!/usr/bin/env python3
import logging
from qtpy.QtWidgets import (
    QApplication,
    QFrame,
    QWidget,
    QGridLayout,
    QPushButton,
)
from qtpy.QtCore import QThreadPool
from siriushlacon.agilent4uhv.agilent import (
    AgilentAsync,
    AgilentAsyncRunnable,
    FIXED as MODE_FIXED,
    STEP as MODE_STEP,
    STEP_TO_FIXED as MODE_STEP_TO_FIXED,
)

from siriushlacon.agilent4uhv.parameters import ParametersFrame
from siriushlacon.agilent4uhv.devices import DevicesFrame

logger = logging.getLogger()


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("VACS - Utility Scripts")

        self.contentLayout = QGridLayout()
        #self.content = QFrame()
        #self.content.setFrameStyle(QFrame.Panel | QFrame.Raised)
        #self.content.setLayout(self.contentLayout)

        # to Step Mode
        self.toStepButton = QPushButton(" to Step ")
        self.toStepButton.setToolTip("Set the voltage behaviour to Step mode.")
        self.toStepButton.clicked.connect(self.toStepAction)
        self.contentLayout.addWidget(self.toStepButton, 0, 0, 1, 1)

        # to Fixed
        self.toFixedButton = QPushButton(" to Fixed ")
        self.toFixedButton.setToolTip(
            "Set the voltage behaviour to Fixed mode and apply a new voltage setpoint."
        )
        self.toFixedButton.clicked.connect(self.toFixedAction)
        self.contentLayout.addWidget(self.toFixedButton, 1, 0, 1, 1)

        # to Step to Fixed
        self.toStepToFixedButton = QPushButton(" to Fixed -> delay -> to Fixed ")
        self.toStepToFixedButton.clicked.connect(self.toStepToFixAction)
        self.toStepToFixedButton.setToolTip(
            "Set the behaviour to Fixed ajusting the channel voltage setpoint, wait n seconds, set the voltage to Fixed applying a new voltage setpoint."
        )
        self.contentLayout.addWidget(self.toStepToFixedButton, 2, 0, 1, 1)

        # Parameters
        self.parameters = ParametersFrame()
        self.parameters.show()
        self.contentLayout.addWidget(self.parameters, 0, 1, 4, 1)

        # Devices
        self.devices = DevicesFrame()
        self.devices.show()
        self.contentLayout.addWidget(self.devices, 5, 0, 1, 2)
        #self.content.show()
        #self.setCentralWidget(self.content)
        self.setLayout(self.contentLayout)

        # Thread !
        self.commandRunning = False

    def debug(self, param):
        self.devices.updateStatus(param)

    def enableComponents(self, enable):
        self.devices.updateDeviceListButton.setEnabled(enable)

        self.toStepButton.setEnabled(enable)
        self.toFixedButton.setEnabled(enable)
        self.toStepToFixedButton.setEnabled(enable)

    def started(self):
        self.commandRunning = True
        self.enableComponents(False)

        self.devices.clearStatus()

    def finished(self):
        self.commandRunning = False
        self.enableComponents(True)

    def toStepAction(self):
        self.doAction(MODE_STEP)

    def toFixedAction(self):
        self.doAction(MODE_FIXED)

    def toStepToFixAction(self):
        self.doAction(MODE_STEP_TO_FIXED)

    def doAction(self, mode):
        if not self.commandRunning:

            agilentAsync = AgilentAsync()
            agilentAsync.timerStatus.connect(self.debug)
            agilentAsync.started.connect(self.started)
            agilentAsync.finished.connect(self.finished)

            runnable = AgilentAsyncRunnable(
                agilentAsync,
                mode=mode,
                voltage=self.parameters.voltage,
                step_to_fixed_delay=self.parameters.delay,
                devices_selection=self.devices.getSelectedDevices(),
            )
            QThreadPool.globalInstance().start(runnable)

def launch():
    app = QApplication([])
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d,%H:%M:%S",
    )

    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    launch()
