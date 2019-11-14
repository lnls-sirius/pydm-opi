import logging

from pydm import Display

from siriushlacon.regatron import proc_alarm
from siriushlacon.regatron.consts import ERR_UI

logger = logging.getLogger()

class Err(Display):
    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, macros=macros, ui_filename=ERR_UI)
        self.btnExtMod.clicked.connect(lambda x: proc_alarm(
            mod=True, std=False, error=True, prefix=macros['P']))
        self.btnExtSys.clicked.connect(lambda x: proc_alarm(
            mod=False, std=False, error=True, prefix=macros['P']))
        self.btnStdMod.clicked.connect(lambda x: proc_alarm(
            mod=True, std=True,  error=True, prefix=macros['P']))
        self.btnStdSys.clicked.connect(lambda x: proc_alarm(
            mod=False, std=True,  error=True, prefix=macros['P']))
