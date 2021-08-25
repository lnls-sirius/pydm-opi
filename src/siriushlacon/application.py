# import multiprocessing
import copy
import enum
import json
import logging
import subprocess
import sys
import typing

import pydm
import pydm.data_plugins
import pydm.utilities
from qtpy.QtWidgets import QMessageBox

from siriushlacon import GENERIC_LAUNCHER_FILE_NAME
from siriushlacon.logging import get_logger

logger = get_logger("")


@enum.unique
class LogLevel(int, enum.Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class SiriushlaconApplication(pydm.PyDMApplication):
    def __init__(
        self,
        ui_file=None,
        command_line_args=None,
        display_args=None,
        perfmon=False,
        hide_nav_bar=False,
        hide_menu_bar=False,
        hide_status_bar=False,
        read_only=False,
        macros=None,
        use_main_window=True,
        stylesheet_path=None,
        fullscreen=False,
    ):
        if not command_line_args:
            command_line_args = []
        if not display_args:
            display_args = []
        super().__init__(
            ui_file=ui_file,
            command_line_args=command_line_args,
            display_args=display_args,
            perfmon=perfmon,
            hide_nav_bar=hide_nav_bar,
            hide_menu_bar=hide_menu_bar,
            hide_status_bar=hide_status_bar,
            read_only=read_only,
            macros=macros,
            use_main_window=use_main_window,
            stylesheet_path=stylesheet_path,
            fullscreen=fullscreen,
        )

        self._generic_launcher_file_name = GENERIC_LAUNCHER_FILE_NAME
        self._generic_launcher_file_path = pydm.utilities.which(
            self._generic_launcher_file_name
        )

        if not self._generic_launcher_file_path:
            logger.error(f"'{self._generic_launcher_file_name}' not found by 'which'")

    def new_pydm_process(self, ui_file, macros=None, command_line_args=None):
        kwargs = copy.deepcopy(
            {
                "displayfile": ui_file,
                "macros": macros,
                "hide_nav_bar": self.hide_nav_bar,
                "hide_menu_bar": self.hide_menu_bar,
                "hide_status_bar": self.hide_status_bar,
                "read_only": pydm.data_plugins.is_read_only(),
            }
        )
        kwargs_str = json.dumps(kwargs)
        python_exe = sys.executable

        if not self._generic_launcher_file_path:
            msg = f"Failed to launch pydm process, '{self._generic_launcher_file_name}' not found in path. Using python '{python_exe}'"
            logger.error(msg)
            box = QMessageBox(QMessageBox.Critical, "New PyDM Process Error", msg)
            box.exec()
            return

        logger.info(f"Init New PyDM Processs - {ui_file}")
        logger.info(f"Params: {kwargs_str}")

        subprocess.Popen(
            [self._generic_launcher_file_path, kwargs_str],
            shell=False,
        )


def launch_pydm(
    displayfile: str,
    macros: typing.Union[str, typing.Dict[str, str]] = None,
    hide_nav_bar: bool = True,
    hide_menu_bar: bool = False,
    hide_status_bar: bool = False,
    fullscreen: bool = False,
    read_only: bool = False,
    perfmon: bool = False,
    log_level: LogLevel = LogLevel.INFO,
    *display_args,
    **kwargs,
):
    _display_args = list(display_args)
    if not macros:
        macros = {}

    from pydm.utilities import setup_renderer

    setup_renderer()

    try:
        """
        We must import QtWebEngineWidgets before creating a QApplication
        otherwise we get the following error if someone adds a WebView at Designer:
        ImportError: QtWebEngineWidgets must be imported before a QCoreApplication instance is created
        """
        from qtpy import QtWebEngineWidgets  # noqa: F401
    except ImportError:
        logger.debug("QtWebEngine is not supported.")

    import pydm
    from pydm.utilities.macro import parse_macro_string

    if macros is not None and type(macros) == str:
        macros = parse_macro_string(macros)

    logger.info("siriushlacon PyDM")
    app = SiriushlaconApplication(
        ui_file=displayfile,
        command_line_args=_display_args,
        perfmon=perfmon,
        hide_nav_bar=hide_nav_bar,
        hide_menu_bar=hide_menu_bar,
        hide_status_bar=hide_status_bar,
        fullscreen=fullscreen,
        read_only=read_only,
        macros=macros,
        stylesheet_path=None,
    )

    pydm.utilities.shortcuts.install_connection_inspector(parent=app.main_window)

    # Qt widgets etc.. must be created after the qapplication
    from siriushlacon.widgets.images import CNPEM_INVISIBLE_LOGO_ICON

    app.setWindowIcon(CNPEM_INVISIBLE_LOGO_ICON)
    sys.exit(app.exec_())
