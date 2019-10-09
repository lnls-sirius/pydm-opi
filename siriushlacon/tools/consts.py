#!/usr/local/env python3
import os
import pkg_resources

def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)

PYDM_TOOLS_PATH = os.path.dirname(get_abs_path('con_tool.py'))

BROWSER_MAIN = get_abs_path('browser.py')
BROWSER_UI = get_abs_path('ui/browser.ui')

VIEWER_URL = 'https://10.0.38.42/archiver-viewer/index.html'
MGMT_URL = 'https://10.0.38.42/mgmt'
BBB_URL = 'https://10.128.255.5/bbb-daemon/index.html'
