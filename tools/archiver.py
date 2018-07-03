from os import path

from pydm import Display


def sslErrorHandler(reply, errorList):
    """Handle SSL errors in the browser.
    Overridden from QWebView.
    Called whenever the browser encounters an SSL error.
    Checks the ssl_mode and responds accordingly.
    """
    reply.ignoreSslErrors()


class MainDisplay(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(MainDisplay, self).__init__(parent=parent, args=args, macros=macros)
        self.args = args
        self.macros = macros
        self.web.page().networkAccessManager().sslErrors.connect(sslErrorHandler)

    def ui_filename(self):
        return 'archiver.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
