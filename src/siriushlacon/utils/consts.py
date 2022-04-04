#!/bin/bash
import datetime
import os
import platform

import pkg_resources
import pytz


def get_abs_path(relative):
    return pkg_resources.resource_filename(__name__, relative)


SP_TZ = pytz.timezone("America/Sao_Paulo")
TIME_ZERO = datetime.timedelta(0)
ARCHIVER_URL: str = "http://10.0.38.42/retrieval/data/getData.json"

IS_LINUX: bool = os.name == "posix" or platform.system() == "Linux"

# ui
OVERVIEW_UI: str = get_abs_path("ui/overview.ui")

BO, SI, TB, TS, IT = "BO", "SI", "TB", "TS", "IT"
