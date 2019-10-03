from qtpy.QtGui import QPixmap

from pydm import Display

from src.mks937b.consts import BTS_UI
from src.utils.consts import BTS_IMG


class BTS(Display):

    def __init__(self, parent=None, args=[], macros=None):
        super(BTS, self).__init__(parent=parent, args=args, macros=macros)

        self.label_pic.setPixmap(QPixmap(BTS_IMG))

    def ui_filename(self):
        return BTS_UI

    def ui_filepath(self):
        return BTS_UI
