import logging as _logging
import typing as _typing

import conscommon.data_model
from qtpy.QtWidgets import QApplication as _QApplication

_logger = _logging.getLogger(__name__)


class LazyDevices:
    """Helper class for lazy loading"""

    def __init__(self, api_get_method):
        self.api_get_method = api_get_method
        self._data: _typing.List[conscommon.data_model.Device] = None

    def get(self) -> _typing.List[conscommon.data_model.Device]:
        if self._data:
            return self._data

        self._data = conscommon.data_model.getDevicesFromBeagles(
            conscommon.data_model.getBeaglesFromList(self.api_get_method())
        )
        return self._data


def close_qt_application(*args, **kwargs):
    app = _QApplication.instance()
    if app:
        _logger.info(f"Closing qt application '{app}'")
        app.quit()
