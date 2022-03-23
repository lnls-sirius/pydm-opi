import typing

from pydm.widgets import PyDMByteIndicator
from qtpy.QtCore import Qt
from qtpy.QtGui import QColor


def get_byte_indicator(
    parent, content: typing.Optional[str], tooltip: str = "", **kwargs
):
    byte = PyDMByteIndicator(parent, content)
    byte.offColor = QColor(59, 0, 0)
    byte.onColor = QColor(255, 0, 0)
    byte.showLabels = False
    byte.orientation = Qt.Horizontal
    byte.numBits = 12
    return byte
