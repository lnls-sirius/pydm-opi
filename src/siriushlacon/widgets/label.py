from pydm.widgets import PyDMLabel
from qtpy.QtCore import Qt

from siriushlacon.widgets.qss import TABLE_ALARMS_QSS

_default_precision = 2


def make_cell_label(
    parent=None,
    content: str = "",
    tooltip: str = "",
    displayFormat: PyDMLabel.DisplayFormat = PyDMLabel.DisplayFormat.Default,
    precision: int = _default_precision,
    showUnits: bool = True,
    precision_from_pv: bool = False,
    alarm_sensitive_border: bool = True,
    alarm_sensitive_content: bool = True,
) -> PyDMLabel:
    if type(precision) != int or precision < 0:
        precision = _default_precision

    lbl = PyDMLabel(parent=parent, init_channel=content)
    lbl.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
    lbl.precisionFromPV = precision_from_pv
    lbl.precision = precision
    lbl.displayFormat = displayFormat
    lbl.showUnits = showUnits
    lbl.alarmSensitiveBorder = alarm_sensitive_border
    lbl.alarmSensitiveContent = alarm_sensitive_content
    lbl.setStyleSheet(TABLE_ALARMS_QSS)
    if precision:
        lbl.precision_changed(precision)
    return lbl
