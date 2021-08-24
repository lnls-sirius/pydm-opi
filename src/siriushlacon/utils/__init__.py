import typing as _typing

import conscommon.data
import conscommon.data_model
from qtpy.QtWidgets import QApplication as _QApplication
from qtpy.QtWidgets import QMessageBox as _QMessageBox

from siriushlacon.logging import get_logger

_logger = get_logger(__name__)


class LazyDevices:
    """Helper class for lazy loading"""

    def __init__(self, api_get_method):
        self.api_get_method = api_get_method
        self._data: _typing.List[conscommon.data_model.Device] = None

    def get(self) -> _typing.List[conscommon.data_model.Device]:
        try:
            if self._data:
                return self._data

            self._data = conscommon.data_model.getDevicesFromBeagles(
                conscommon.data_model.getBeaglesFromList(self.api_get_method())
            )
            return self._data
        except Exception as e:
            _logger.exception("Failed to acquire data from the API")
            _QMessageBox.critical(
                None,
                "Beaglebone Info API Error",
                f"Failed to get information from the remote API. Check if the server is reachable at {conscommon.data.API_CANDIDATES}.\nError '{e}'",
            )
            raise e


def close_qt_application(*args, **kwargs):
    app = _QApplication.instance()
    if app:
        _logger.info(f"Closing qt application '{app}'")
        app.quit()
