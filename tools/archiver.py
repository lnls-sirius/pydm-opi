#!/usr/bin/python3

from os import path, environ

from pydm import Display 
#from pydm.PyQt import Qt
#import PyQt5
#from PyQt5.QtCore import QUrl
#from PyQt5.QtWebKit import QWebView

def sslErrorHandler(reply, errorList):
    """Handle SSL errors in the browser.
    Overridden from QWebView.
    Called whenever the browser encounters an SSL error.
    Checks the ssl_mode and responds accordingly.
    """
    reply.ignoreSslErrors()


class MainDisplay(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(MainDisplay, self).__init__(
            parent=parent, args=args, macros=macros)
        
        self.args = args
        self.macros = macros
        # print('type {}'.format(type(self.timeEdit))) 
        self.web.page().networkAccessManager().sslErrors.connect(sslErrorHandler)

    def ui_filename(self):
        return '../../../tools/archiver.ui'

    def ui_filepath(self): 
        return path.join(path.dirname(path.realpath(__file__)), 'archiver.ui')
