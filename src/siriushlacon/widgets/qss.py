import pkg_resources


def get_abs_path(relative):
    return pkg_resources.resource_filename(__name__, relative)


TABLE_ALARMS_QSS: str = ""
with open(get_abs_path("resources/css/table-alarm.qss")) as f:
    TABLE_ALARMS_QSS = "".join(f.readlines())
