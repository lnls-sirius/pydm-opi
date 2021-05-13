from pydm import Display
from qtpy.QtGui import QPixmap

from siriushlacon.mks937b.consts import (
    MKS_LAUNCH_UI,
    MKS_OVERVIEW,
    LTB_UI,
    BOOSTER_UI,
    BTS_UI,
    STORAGE_RING_UI,
)
from siriushlacon.utils.consts import CNPEM_IMG, LNLS_IMG


class MksLauncher(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(MksLauncher, self).__init__(parent=parent, args=args, macros=macros)

        self.btnOverview.filenames = [MKS_OVERVIEW]
        self.btnOverview.openInNewWindow = True

        self.btnRing.filenames = [STORAGE_RING_UI]
        self.btnRing.openInNewWindow = True

        self.btnBooster.filenames = [BOOSTER_UI]
        self.btnBooster.openInNewWindow = True

        self.btnLtb.filenames = [LTB_UI]
        self.btnLtb.openInNewWindow = True

        self.btnBts.filenames = [BTS_UI]
        self.btnBts.openInNewWindow = True

        self.label_cnpem.setPixmap(QPixmap(CNPEM_IMG))
        self.label_lnls.setPixmap(QPixmap(LNLS_IMG))

    def ui_filename(self):
        return MKS_LAUNCH_UI

    def ui_filepath(self):
        return MKS_LAUNCH_UI
