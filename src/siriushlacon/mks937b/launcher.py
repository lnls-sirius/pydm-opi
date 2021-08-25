from pydm import Display

from siriushlacon.mks937b.consts import (
    BOOSTER_UI,
    BTS_UI,
    LTB_UI,
    MKS_LAUNCH_UI,
    MKS_OVERVIEW,
    STORAGE_RING_UI,
)
from siriushlacon.widgets.images import CNPEM_PIXMAP, LNLS_PIXMAP


class MksLauncher(Display):
    def __init__(self, parent=None, args=None, macros=None):
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

        self.label_cnpem.setPixmap(CNPEM_PIXMAP)
        self.label_lnls.setPixmap(LNLS_PIXMAP)

    def ui_filename(self):
        return MKS_LAUNCH_UI

    def ui_filepath(self):
        return MKS_LAUNCH_UI
