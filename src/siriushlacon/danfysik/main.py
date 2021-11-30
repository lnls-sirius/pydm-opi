import logging

from pydm import Display

from siriushlacon.danfysik.consts import DANSYFIK_MAIN_UI

logger = logging.getLogger()


class DanfysikMain(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(DanfysikMain, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=DANSYFIK_MAIN_UI
        )
