import pkg_resources


def get_abs_path(filename):
    return pkg_resources.resource_filename(__name__, filename)


EPICSTEL_MAIN = get_abs_path("main.py")
EPICSTEL_MAIN_UI = get_abs_path("ui/main.ui")
EPICSTEL_LOGIN_UI = get_abs_path("ui/login.ui")
EPICSTEL_USER_UI = get_abs_path("ui/user.ui")
EPICSTEL_TEAM_UI = get_abs_path("ui/team.ui")
EPICSTEL_PV_UI = get_abs_path("ui/pv.ui")
EPICSTEL_ITEMS_UI = get_abs_path("ui/editlist.ui")

EPICSTEL_TABS = ["pvs", "users", "teams"]

EPICSTEL_HOST = "mongodb://10.0.38.46:27040/"
