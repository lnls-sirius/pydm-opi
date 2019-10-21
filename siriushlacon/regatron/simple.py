import logging
import json
from pydm import Display

from siriushlacon.regatron.consts import SIMPLE_UI, ERR_MAIN, WARN_MAIN

logger = logging.getLogger()

logger = logging.getLogger()

class Simple(Display):
    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, macros=macros, ui_filename=SIMPLE_UI)

        self.btnErr.filenames = [ERR_MAIN]
        self.btnErr.macros = [json.dumps(macros)]
        self.btnErr.openInNewWindow = True
        self.btnErr.showIcon = False

        self.btnWarn.filenames = [WARN_MAIN]
        self.btnWarn.macros = [json.dumps(macros)]
        self.btnWarn.openInNewWindow = True
        self.btnWarn.showIcon = False