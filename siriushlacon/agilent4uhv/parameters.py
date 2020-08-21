import logging
import re
from qtpy.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from qtpy.QtGui import QDoubleValidator, QIntValidator, QRegExpValidator
from qtpy.QtCore import QRegExp


logger = logging.getLogger()

MIN_SEC_PATTERN = r"^([0-5]?[0-9]):([0-5]?[0-9])$"
MIN_SEC_REG = re.compile(MIN_SEC_PATTERN)


class ParametersFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super(ParametersFrame, self).__init__(*args, **kwargs)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.contentLayout = QGridLayout()

        self.setpointVoltageLabel = QLabel("Fixed voltage [3000 to 7000] V")
        self.setpointVoltageSettingLabel = QLabel()
        self.setpointVoltageInp = QLineEdit()
        self.setpointVoltageInp.setMaximumWidth(100)
        self.setpointVoltageInp.setValidator(QIntValidator(3000, 7000))
        self.setpointVoltageInp.setToolTip("Final voltage setpoint.")
        self.setpointVoltageInp.setText("3000")
        self.contentLayout.addWidget(self.setpointVoltageLabel, 0, 0, 1, 1)
        self.contentLayout.addWidget(self.setpointVoltageInp, 0, 1, 1, 1)
        self.contentLayout.addWidget(self.setpointVoltageSettingLabel, 0, 2, 1, 1)

        self.stepToFixDelayLabel = QLabel("Step to Fixed delay (mm:ss)")
        self.stepToFixDelaySettingLabel = QLabel()
        self.stepToFixDelayInp = QLineEdit()
        self.stepToFixDelayInp.setMaximumWidth(100)
        self.stepToFixDelayInp.setValidator(QRegExpValidator(QRegExp(MIN_SEC_PATTERN)))
        self.stepToFixDelayInp.setToolTip("Delay between toStep and toFixed calls.")
        self.stepToFixDelayInp.setText("05:00")

        self.contentLayout.addWidget(self.stepToFixDelayLabel, 1, 0, 1, 1)
        self.contentLayout.addWidget(self.stepToFixDelayInp, 1, 1, 1, 1)
        self.contentLayout.addWidget(self.stepToFixDelaySettingLabel, 1, 2, 1, 1)

        self.setButton = QPushButton("Confirm")
        self.setButton.clicked.connect(self.confirm)
        self.setButton.setToolTip("Apply settings")
        self.contentLayout.addWidget(self.setButton, 3, 1, 1, 1)

        self.setLayout(self.contentLayout)
        self.confirm()

    def confirm(self):
        try:
            voltageString = self.setpointVoltageInp.text()
            tmp = int(voltageString)
            self.voltage = 3000 if tmp < 3000 else (7000 if tmp > 7000 else tmp)
            self.setpointVoltageSettingLabel.setText("{} V".format(self.voltage))
        except ValueError:
            pass

        try:
            delayString = self.stepToFixDelayInp.text()
            if MIN_SEC_REG.match(delayString):
                res = MIN_SEC_REG.search(delayString)
                self.delay = 60 * float(res.group(1)) + float(res.group(2))
                self.stepToFixDelaySettingLabel.setText(
                    "{} mm:ss ({}s)".format(delayString, self.delay)
                )
        except ValueError:
            pass
