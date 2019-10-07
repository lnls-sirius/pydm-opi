#!/usr/bin/python3
import logging
from pydm import Display
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebInspector
from PyQt5.QtNetwork import QSslConfiguration, QSsl, QSslSocket

from siriushlacon.tools.consts import BROWSER_UI

logger = logging.getLogger()

def sslErrorHandler(reply, errorList):
    """Handle SSL errors in the browser.
    Overridden from QWebView.
    Called whenever the browser encounters an SSL error.
    Checks the ssl_mode and responds accordingly.
    """
    for e in errorList:
        logger.error('{}'.format(e.errorString() ))
    reply.ignoreSslErrors()



class MainDisplay(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(MainDisplay, self).__init__(
            parent=parent, args=args, macros=macros, ui_filename=BROWSER_UI)

        sslCfg = QSslConfiguration.defaultConfiguration()
        sslCfg.setProtocol(QSsl.AnyProtocol)
        sslCfg.setPeerVerifyMode(QSslSocket.VerifyNone)
        QSslConfiguration.setDefaultConfiguration(sslCfg)

        self.args = args
        self.macros = macros
        self.web.settings().setAttribute(
            QWebSettings.DeveloperExtrasEnabled, True)
        self.web.page().networkAccessManager().sslErrors.connect(sslErrorHandler)

        #self.inspect = QWebInspector()
        #self.inspect.setPage(self.web.page())
        #self.inspect.show()