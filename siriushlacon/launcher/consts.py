import pkg_resources


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


LAUNCH_WINDOW = get_abs_path("launcher.py")
LAUNCH_WINDOW_UI = get_abs_path("ui/launcher.ui")

PCTRL_MAIN = get_abs_path("../pctrl/main.py")
