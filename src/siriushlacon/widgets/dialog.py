import typing as _typing

from pydm.display import Display as _Display
from qtpy import QtCore as _QtCore
from qtpy.QtWidgets import QDialog as _QDialog
from qtpy.QtWidgets import QGridLayout as _QGridLayout
from qtpy.QtWidgets import QWidget as _QWidget

from siriushlacon import DEFAULT_WINDOW_TITLE as _DEFAULT_WINDOW_TITLE
from siriushlacon.widgets.images import (
    CNPEM_INVISIBLE_LOGO_ICON as _CNPEM_INVISIBLE_LOGO_ICON,
)


class BaseDialog(_QDialog):
    """Base modal dialog"""

    def __init__(
        self,
        parent: _typing.Optional[_QWidget],
        flags: _typing.Union[
            _QtCore.Qt.WindowFlags, _QtCore.Qt.WindowType
        ] = _QtCore.Qt.Dialog,
        window_title: str = _DEFAULT_WINDOW_TITLE,
        macros: _typing.Optional[_typing.Dict[str, str]] = None,
    ) -> None:
        super().__init__(parent=parent, flags=flags)
        self.setModal(True)
        self.setWindowTitle(window_title)
        self.setWindowIcon(_CNPEM_INVISIBLE_LOGO_ICON)
        self.setWindowModality(_QtCore.Qt.WindowModal)
        self.setWindowState(_QtCore.Qt.WindowActive)

        self._display: _typing.Optional[_Display] = None

    def set_display(self, display: _Display):
        if not self.layout() and not self._display:
            self._display = display
            layout = _QGridLayout(self)
            layout.addWidget(self._display, 0, 0)

            self.setLayout(layout)
            self.adjustSize()
