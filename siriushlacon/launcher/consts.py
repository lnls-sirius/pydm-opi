import os


# Consts
def get_abs_path(filename):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)


LAUNCH_WINDOW = get_abs_path('launcher.py')
LAUNCH_WINDOW_UI = get_abs_path('ui/launcher.ui')

PCTRL_MAIN = '../pctrl/main.py'

# EPP_MAIN = '../ui/spixconv/launch_ui_main_window.py'
