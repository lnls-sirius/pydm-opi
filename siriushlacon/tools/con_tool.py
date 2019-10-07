#!/usr/bin/python3
from os import path

from pydm.tools import ExternalTool
from pydm.utilities.iconfont import IconFont

from siriushlacon.tools.consts import BROWSER_MAIN


def get_abs_path(relative):
    """
    relative = relative path with base at python/
    """
    return path.join(path.dirname(path.realpath(__file__)), relative)


class ArchiverApplianceTool(ExternalTool):

    def __init__(self):
        icon = IconFont().icon("archive")
        name = 'Archiver Appliance'
        group = 'CON'
        use_with_widgets = False
        ExternalTool.__init__(self, icon=icon, name=name, group=group,
                              use_with_widgets=use_with_widgets)

    def call(self, channels, sender):
        sender.window().new_window(
            get_abs_path(BROWSER_MAIN),
            macros={'url': 'https://10.0.38.42/mgmt'})

    def to_json(self):
        return ""

    def from_json(self, content):
        print("Received from_json: ", content)

    def get_info(self):
        ret = ExternalTool.get_info(self)
        ret.update({'file': __file__})
        return ret


class ArchiverViwerTool(ExternalTool):

    def __init__(self):
        icon = IconFont().icon('desktop')
        name = 'Archiver Viwer'
        group = 'CON'
        use_with_widgets = False
        ExternalTool.__init__(self, icon=icon, name=name, group=group,
                              use_with_widgets=use_with_widgets)

    def call(self, channels, sender):
        url = 'https://10.0.38.42/archiver-viewer/index.html'
        sender.window().new_window(
            get_abs_path(BROWSER_MAIN),
            macros={'url': url})

    def to_json(self):
        return ""

    def from_json(self, content):
        print("Received from_json: ", content)

    def get_info(self):
        ret = ExternalTool.get_info(self)
        ret.update({'file': __file__})
        return ret


class BeagleboneTool(ExternalTool):

    def __init__(self):
        icon = IconFont().icon('paw')
        name = 'Beaglebone Daemon'
        group = 'CON'
        use_with_widgets = False
        ExternalTool.__init__(self, icon=icon, name=name, group=group,
                              use_with_widgets=use_with_widgets)

    def call(self, channels, sender):
        sender.window().new_window(get_abs_path(BROWSER_MAIN),
        macros={'url':'https://10.128.255.5/bbb-daemon/index.html'})

    def to_json(self):
        return ""

    def from_json(self, content):
        print("Received from_json: ", content)

    def get_info(self):
        ret = ExternalTool.get_info(self)
        ret.update({'file': __file__})
        return ret
