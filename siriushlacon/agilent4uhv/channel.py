import logging
from pydm import Display

from siriushlacon.agilent4uhv.consts import AGILENT_CHANNEL_UI

logger = logging.getLogger()

class Channel(Display):

    def __init__(self, parent=None, args=[], macros=None):
        super(Channel, self).__init__(parent=parent, args=args,
                                      macros=macros, ui_filename=AGILENT_CHANNEL_UI)

        logger.info('Channel macros {}'.format(macros))
