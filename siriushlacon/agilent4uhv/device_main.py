
import json

from pydm import Display
from qtpy.QtGui import QPixmap

from siriushlacon.agilent4uhv.consts import AGILENT_DEVICE_MAIN_UI, \
    AGILENT_DEVICE_UI, AGILENT_CHANNEL_UI
from siriushlacon.utils.consts import CNPEM_IMG, LNLS_IMG


class DeviceMain(Display):

    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMain, self).__init__(parent=parent, args=args,
                                         macros=macros)

        self.btn_device.filenames = [AGILENT_DEVICE_UI]
        self.btn_device.macros = json.dumps({"PREFIX": macros["DEVICE"]})
        self.btn_device.openInNewWindow = True

        self.btn_ch1.filenames = [AGILENT_CHANNEL_UI]
        self.btn_ch1.macros = json.dumps({"PREFIX": macros["PREFIX_C1"]})
        self.btn_ch1.openInNewWindow = True

        self.btn_ch2.filenames = [AGILENT_CHANNEL_UI]
        self.btn_ch2.macros = json.dumps({"PREFIX": macros["PREFIX_C3"]})
        self.btn_ch2.openInNewWindow = True

        self.btn_ch3.filenames = [AGILENT_CHANNEL_UI]
        self.btn_ch3.macros = json.dumps({"PREFIX": macros["PREFIX_C3"]})
        self.btn_ch3.openInNewWindow = True

        self.btn_ch4.filenames = [AGILENT_CHANNEL_UI]
        self.btn_ch4.macros = json.dumps({"PREFIX": macros["PREFIX_C4"]})
        self.btn_ch4.openInNewWindow = True

        self.label_cnpem.setPixmap(QPixmap(CNPEM_IMG))
        self.label_lnls.setPixmap(QPixmap(LNLS_IMG))

    def ui_filename(self):
        return AGILENT_DEVICE_MAIN_UI

    def ui_filepath(self):
        return AGILENT_DEVICE_MAIN_UI
