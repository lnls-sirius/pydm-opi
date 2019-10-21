import logging
from pydm import Display

from siriushlacon.regatron import proc_alarm
from siriushlacon.regatron.consts import WARN_UI

logger = logging.getLogger()

class Err(Display):
    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, macros=macros, ui_filename=WARN_UI)
        self.btnExtMod.clicked.connect(lambda x:proc_alarm(mod=True, std=False, error=False, prefix=macros['P']))
        self.btnExtSys.clicked.connect(lambda x:proc_alarm(mod=False,std=False, error=False, prefix=macros['P']))
        self.btnStdMod.clicked.connect(lambda x:proc_alarm(mod=True, std=True,  error=False, prefix=macros['P']))
        self.btnStdSys.clicked.connect(lambda x:proc_alarm(mod=False,std=True,  error=False, prefix=macros['P']))