import logging
from qtpy.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from qtpy.QtGui import (
    QDoubleValidator,
    QIntValidator,
)


logger = logging.getLogger()


class ParametersFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super(ParametersFrame, self).__init__(*args, **kwargs)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.contentLayout = QGridLayout()

        self.voltage = 3000
        self.delay = 600.00

        self.setpointVoltageLabel = QLabel("Fixed voltage [3000 to 7000] V")
        self.setpointVoltageSettingLabel = QLabel()
        self.setpointVoltageInp = QLineEdit()
        self.setpointVoltageInp.setMaximumWidth(100)
        self.setpointVoltageInp.setValidator(QIntValidator(3000, 7000))
        self.setpointVoltageInp.setToolTip("New fixed voltage setpoint.")

        self.contentLayout.addWidget(self.setpointVoltageLabel, 0, 0, 1, 1)
        self.contentLayout.addWidget(self.setpointVoltageInp, 0, 1, 1, 1)
        self.contentLayout.addWidget(self.setpointVoltageSettingLabel, 0, 2, 1, 1)

        self.stepToFixDelayLabel = QLabel("Step to Fixed delay in seconds")
        self.stepToFixDelaySettingLabel = QLabel()
        self.stepToFixDelayInp = QLineEdit()
        self.stepToFixDelayInp.setMaximumWidth(100)
        self.stepToFixDelayInp.setValidator(QDoubleValidator(1, 1440, 2))
        self.stepToFixDelayInp.setToolTip("Delay between toStep and toFixed calls.")

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
        except ValueError:
            pass
        finally:
            self.setpointVoltageSettingLabel.setText("{} V".format(self.voltage))
        try:
            delayString = self.stepToFixDelayInp.text()
            tmp = float(delayString)
            self.delay = 1.0 if tmp < 1.0 else (1440.0 if tmp > 1440.0 else tmp)
        except ValueError:
            pass
        finally:
            self.stepToFixDelaySettingLabel.setText("{} s".format(self.delay))
