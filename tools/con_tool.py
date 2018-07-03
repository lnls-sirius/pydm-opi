from pydm.tools import ExternalTool
from pydm.utilities.iconfont import IconFont


class ArchiverApplianceTool(ExternalTool):

    def __init__(self):
        icon = IconFont().icon("archive")
        name = 'Archiver Appliance'
        group = 'CON'
        use_with_widgets = False
        ExternalTool.__init__(self, icon=icon, name=name, group=group, use_with_widgets=use_with_widgets)

    def call(self, channels, sender):
        sender.window().new_window('archiver.py', macros={'url': 'https://10.0.4.57:11995/mgmt/ui/index.html'})

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
        ExternalTool.__init__(self, icon=icon, name=name, group=group, use_with_widgets=use_with_widgets)

    def call(self, channels, sender):
        sender.window().new_window('archiver.py',
                                   macros={'url': 'http://10.0.4.57:11998/retrieval/ui/archiver-viewer/index.html'})

    def to_json(self):
        return ""

    def from_json(self, content):
        print("Received from_json: ", content)

    def get_info(self):
        ret = ExternalTool.get_info(self)
        ret.update({'file': __file__})
        return ret


class BeableboneTool(ExternalTool):

    def __init__(self):
        icon = IconFont().icon('paw')
        name = 'Beaglebone Daemon'
        group = 'CON'
        use_with_widgets = False
        ExternalTool.__init__(self, icon=icon, name=name, group=group, use_with_widgets=use_with_widgets)

    def call(self, channels, sender):
        sender.window().new_window('bbb.ui', macros={})

    def to_json(self):
        return ""

    def from_json(self, content):
        print("Received from_json: ", content)

    def get_info(self):
        ret = ExternalTool.get_info(self)
        ret.update({'file': __file__})
        return ret
