import pkg_resources


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


DANSYFIK_MAIN_UI = get_abs_path("ui/main.ui")
DANSYFIK_MAIN_PY = get_abs_path("main.py")
