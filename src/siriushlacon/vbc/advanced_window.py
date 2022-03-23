#!/usr/bin/env python3

from pydm import Display

from siriushlacon.vbc.confirmation_message import ConfirmationMessageDialog
from siriushlacon.vbc.consts import ADVANCED_WINDOW_UI
from siriushlacon.widgets.images import CNPEM_PIXMAP, LNLS_PIXMAP


class DeviceMenu(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(DeviceMenu, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=ADVANCED_WINDOW_UI
        )
        self.lnlsLabel.setPixmap(LNLS_PIXMAP)
        self.lnlsLabel.setFixedSize(LNLS_PIXMAP.size())

        self.cnpemLabel.setPixmap(CNPEM_PIXMAP)
        self.cnpemLabel.setFixedSize(CNPEM_PIXMAP.size())

        self.prefix = macros["IOC"]
        self.PyDMCheckbox_Relay1.clicked.connect(lambda *_: self._relay_popup(1))
        self.PyDMCheckbox_Relay2.clicked.connect(lambda *_: self._relay_popup(2))
        self.PyDMCheckbox_Relay3.clicked.connect(lambda *_: self._relay_popup(3))
        self.PyDMCheckbox_Relay4.clicked.connect(lambda *_: self._relay_popup(4))
        self.PyDMCheckbox_Relay5.clicked.connect(lambda *_: self._relay_popup(5))

    def _relay_popup(self, number: int, *_):
        dialog = ConfirmationMessageDialog(
            parent=self, macros=self.macros(), relay_number=number, prefix=self.prefix
        )
        dialog.show()
