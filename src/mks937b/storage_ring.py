from qtpy.QtGui import QPixmap

from pydm import Display

from src.mks937b.consts import STORAGE_RING_UI
from src.utils.consts import RINGB1A_IMG, RINGB2A_IMG


class StorageRing(Display):

    def __init__(self, parent=None, args=[], macros=None):
        super(StorageRing, self).__init__(parent=parent, args=args,
                                          macros=macros)

        self.label_pic1.setPixmap(QPixmap(RINGB1A_IMG))
        self.label_pic2.setPixmap(QPixmap(RINGB2A_IMG))

    def ui_filename(self):
        return STORAGE_RING_UI

    def ui_filepath(self):
        return STORAGE_RING_UI
