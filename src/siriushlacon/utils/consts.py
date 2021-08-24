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

# Images
CNPEM_IMG: str = get_abs_path("images/CNPEM.jpg")
CNPEM_INVISIBLE_IMG: str = get_abs_path("images/CNPEM-invisible.png")
CNPEM_INVISIBLE_LOGO_IMG: str = get_abs_path("images/CNPEM-invisible-logo.png")
LNLS_IMG: str = get_abs_path("images/sirius-hla-as-cons-lnls.png")

LNLS_INVISIBLE_IMG: str = get_abs_path("images/lnls-invisible.png")
LTB_IMG: str = get_abs_path("images/ltb.png")
BOOSTER_IMG: str = get_abs_path("images/booster.png")
BTS_IMG: str = get_abs_path("images/btts.png")
STORAGE_RING_IMG: str = get_abs_path("images/storage_ring.png")
RINGB1A_IMG: str = get_abs_path("images/ringB1A.png")
RINGB2A_IMG: str = get_abs_path("images/ringB2A.png")

BO, SI, TB, TS = "BO", "SI", "TB", "TS"
