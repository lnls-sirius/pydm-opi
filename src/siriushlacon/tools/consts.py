#!/usr/local/env python3
import os

import pkg_resources


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


PYDM_TOOLS_PATH = os.path.dirname(get_abs_path("con_tool.py"))

VIEWER_URL = "https://10.0.38.42/archiver-viewer/index.html"
MGMT_URL = "https://10.0.38.42/mgmt"
BBB_URL = "https://10.0.38.42/bbb-daemon/index.html"
