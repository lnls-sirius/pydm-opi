from qtpy.QtGui import QPixmap

from pydm import Display

from siriushlacon.mks937b.consts import BOOSTER_UI
from siriushlacon.utils.consts import BOOSTER_IMG


class Booster(Display):

    def __init__(self, parent=None, args=[], macros=None):
        super(Booster, self).__init__(parent=parent, args=args,
                                      macros=macros)

        self.label_pic.setPixmap(QPixmap(BOOSTER_IMG))

    def ui_filename(self):
        return BOOSTER_UI

    def ui_filepath(self):
        return BOOSTER_UI
