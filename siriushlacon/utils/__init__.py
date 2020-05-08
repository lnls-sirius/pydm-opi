from typing import List
import conscommon.data_model


class LazyDevices:
    """ Helper class for lazy loading """

    _data = None

    def __init__(self, api_get_method):
        self.api_get_method = api_get_method

    def get(self) -> List[conscommon.data_model.Device]:
        if not self._data:
            self._data = conscommon.data_model.getDevicesFromBeagles(
                conscommon.data_model.getBeaglesFromList(self.api_get_method())
            )
        return self._data
