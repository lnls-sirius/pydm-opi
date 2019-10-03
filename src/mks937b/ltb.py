from qtpy.QtGui import QPixmap

from pydm import Display

from src.mks937b.consts import LTB_UI
from src.utils.consts import LTB_IMG


class LTB(Display):

    def __init__(self, parent=None, args=[], macros=None):
        super(LTB, self).__init__(parent=parent, args=args, macros=macros)

        self.label_pic.setPixmap(QPixmap(LTB_IMG))

    def ui_filename(self):
        return LTB_UI

    def ui_filepath(self):
        return LTB_UI
