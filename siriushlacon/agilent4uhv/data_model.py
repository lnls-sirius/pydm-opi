from typing import List, Tuple, Iterable


class Channel:
    def __init__(
        self, name: str = "", prefix: str = "", num: int = 0, config: list = []
    ):
        self.list = config
        self.name = name
        self.num = num
        self.prefix = prefix

    def __repr__(self):
        return "{}(prefix={},name={})".format(
            self.__class__.__name__, self.prefix, self.name
        )


class Device:
    def __init__(
        self, prefix: str = "", info: dict = {}, channels: dict = {}, enable=True
    ):
        self.enable = enable
        self.info = info
        self.prefix = prefix
        self.channels: List[Channel] = []
        self._generateChannels(channels)

    def getChannelByPrefix(self, prefix: str) -> Channel:
        for channel in self.channels:
            if channel.prefix == prefix:
                return

    def _generateChannels(self, data):
        for k, v in data.items():
            if v.__class__.__name__ == Channel.__class__.__name__:
                self.channels.append(v)
            else:
                self.channels.append(Channel(name=k, **v))

    def __repr__(self):
        return "{}(prefix={},enabled={})".format(
            self.__class__.__name__, self.prefix, self.enable
        )


class Beaglebone:
    def __init__(self, ip: str = "", devices: list = []):
        self.ip = ip
        self.devices: List[Device] = []
        self._generateDevices(devices)

    def _generateDevices(self, data):
        for d in data:
            if d.__class__.__name__ == Device.__class__.__name__:
                self.devices.append(d)
            else:
                self.devices.append(Device(**d))

    def __repr__(self):
        return "{}(ip={},devices={})".format(
            self.__class__.__name__, self.ip, self.devices
        )


def getDevicesFromBeagles(beagles: List[Beaglebone],) -> List[Device]:
    """ Generate devices from beagle """
    devices: List[Device] = []
    for beagle in beagles:
        for device in beagle.devices:
            devices.append(device)
    return devices


# def iterateBeagleDevices(
#    beagles: List[Beaglebone.__class__],
# ) -> Iterable[Tuple[Beaglebone, Device]]:
#    """ Generate devices from beagle """
#    for beagle in beagles:
#        for device in beagle.devices:
#            yield beagle, device


def getDevicesFromList(data: list) -> List[Device]:
    """ Load datamodel objects from a list of dictionaries """
    devices: List[Device] = []
    for d in data:
        devices.append(Device(**d))
    return devices


def getBeaglesFromList(data: dict) -> List[Beaglebone]:
    """ Load datamodel objects from dictionary """
    beagles: List[Beaglebone] = []
    for k, v in data.items():
        beagle = Beaglebone(ip=k, devices=v)
        beagles.append(beagle)

    return beagles
