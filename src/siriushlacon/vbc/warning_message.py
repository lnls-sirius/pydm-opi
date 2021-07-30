#!/usr/bin/env python3
import sys
import typing as _typing

from pydm import Display
from pydm.widgets.byte import PyDMByteIndicator
from pydm.widgets.checkbox import PyDMCheckbox
from pydm.widgets.label import PyDMLabel
from qtpy.QtWidgets import QDialogButtonBox, QLabel, QWidget

from siriushlacon.utils import close_qt_application
from siriushlacon.utils.command_runner import CommandRunner, ShellCommandRunner
from siriushlacon.utils.dialog import BaseDialog as _BaseDialog
from siriushlacon.utils.images import LNLS_PIXMAP
from siriushlacon.vbc.consts import OK_MESSAGE_PY, WARNING_WINDOW_UI
from siriushlacon.vbc.scripts import process_recovery


class VBCWarningMessage(Display):
    def _close(self):
        if self.parent() and isinstance(self.parent(), QWidget):
            self.parent().close()
        else:
            close_qt_application()

    def __init__(
        self,
        parent=None,
        args=None,
        macros=None,
        prefix: _typing.Optional[str] = None,
    ):
        super(VBCWarningMessage, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=WARNING_WINDOW_UI
        )
        IOC = prefix if prefix else str(sys.argv[5])
        self.Stage_1: PyDMByteIndicator
        self.Stage_2: PyDMByteIndicator
        self.Stage_3: PyDMByteIndicator
        self.Stage_4: PyDMByteIndicator
        self.Stage_5: PyDMByteIndicator

        self.pressure_base: PyDMLabel
        self.pressure_exp: PyDMLabel

        self.Shell_PV_Trigger_OK_MESSAGE: PyDMCheckbox
        self.buttonBox_2: QDialogButtonBox
        self.label_9: QLabel

        # defining macro for PyDMShellCommand (for launching "warning_message.ui")
        self.Stage_1.channel = f"ca://{IOC}:ProcessRecovery:Status1"
        self.Stage_2.channel = f"ca://{IOC}:ProcessRecovery:Status2"
        self.Stage_3.channel = f"ca://{IOC}:ProcessRecovery:Status3"
        self.Stage_4.channel = f"ca://{IOC}:ProcessRecovery:Status4"
        self.Stage_5.channel = f"ca://{IOC}:ProcessRecovery:Status5"
        self.pressure_base.channel = f"ca://{IOC}:BBB:TorrBaseMsg"
        self.pressure_exp.channel = f"ca://{IOC}:BBB:TorrExpMsg"

        self.label_9.setPixmap(LNLS_PIXMAP)
        self.label_9.setFixedSize(LNLS_PIXMAP.size())

        self.ProcessRecoveryCommand = CommandRunner(
            command=lambda: process_recovery(IOC), name="ProcessRecovery"
        )
        self.OkMessageCommand = ShellCommandRunner(
            command=f"pydm --hide-nav-bar --hide-menu-bar --hide-status-bar {OK_MESSAGE_PY} {IOC} REC"
        )

        self.Shell_PV_Trigger_OK_MESSAGE.setVisible(False)
        self.Shell_PV_Trigger_OK_MESSAGE.toggled.connect(
            lambda *_: self.OkMessageCommand.execute_command()
        )
        self.Shell_PV_Trigger_OK_MESSAGE.toggled.connect(self._close)

        self.buttonBox_2.accepted.connect(
            lambda *_: self.ProcessRecoveryCommand.execute_command()
        )
        self.buttonBox_2.rejected.connect(self._close)


class VBCWarningMessageDialog(_BaseDialog):
    def __init__(
        self,
        parent: _typing.Optional[QWidget],
        macros: _typing.Optional[_typing.Dict[str, str]],
        prefix: str,
    ) -> None:
        super().__init__(parent=parent, window_title="VBC - Warning Message")
        display = VBCWarningMessage(
            parent=self, prefix=prefix, macros=macros if macros else {}
        )
        self.set_display(display)
