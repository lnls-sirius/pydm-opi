import pkg_resources
from qtpy.QtGui import QIcon, QPixmap


def get_abs_path(relative):
    return pkg_resources.resource_filename(__name__, relative)


_CNPEM_IMG: str = get_abs_path("resources/images/CNPEM.jpg")
_CNPEM_INVISIBLE_IMG: str = get_abs_path("resources/images/CNPEM-invisible.png")
_CNPEM_INVISIBLE_LOGO_IMG: str = get_abs_path(
    "resources/images/CNPEM-invisible-logo.png"
)
_LNLS_IMG: str = get_abs_path("resources/images/sirius-hla-as-cons-lnls.png")
_LNLS_INVISIBLE_IMG: str = get_abs_path("resources/images/lnls-invisible.png")

CNPEM_PIXMAP: QPixmap = QPixmap(_CNPEM_IMG)
CNPEM_ICON: QIcon = QIcon(CNPEM_PIXMAP)

CNPEM_INVISIBLE_PIXMAP: QPixmap = QPixmap(_CNPEM_INVISIBLE_IMG)
CNPEM_INVISIBLE_ICON: QIcon = QIcon(CNPEM_INVISIBLE_PIXMAP)

CNPEM_INVISIBLE_LOGO_PIXMAP: QPixmap = QPixmap(_CNPEM_INVISIBLE_LOGO_IMG)
CNPEM_INVISIBLE_LOGO_ICON: QIcon = QIcon(CNPEM_INVISIBLE_LOGO_PIXMAP)

LNLS_PIXMAP: QPixmap = QPixmap(_LNLS_IMG)
LNLS_ICON: QIcon = QIcon(LNLS_PIXMAP)

LNLS_INVISIBLE_PIXMAP: QPixmap = QPixmap(_LNLS_INVISIBLE_IMG)
LNLS_INVISIBLE_ICON: QIcon = QIcon(LNLS_INVISIBLE_PIXMAP)
