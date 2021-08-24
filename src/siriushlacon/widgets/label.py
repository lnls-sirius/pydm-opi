from pydm.widgets import PyDMLabel

from siriushlacon.widgets.qss import TABLE_ALARMS_QSS


def get_label(
    parent=None,
    content: str = "",
    tooltip: str = "",
    displayFormat: PyDMLabel.DisplayFormat = PyDMLabel.DisplayFormat.Default,
    precision: int = 2,
    showUnits: bool = True,
):
    lbl = PyDMLabel(parent=parent, init_channel=content)
    lbl.precisionFromPV = False
    lbl.precision = precision
    lbl.displayFormat = displayFormat
    lbl.showUnits = showUnits
    lbl.alarmSensitiveBorder = True
    lbl.alarmSensitiveContent = True
    lbl.setStyleSheet(TABLE_ALARMS_QSS)
    if precision:
        lbl.precision_changed(precision)
    return lbl
