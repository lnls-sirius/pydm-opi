import copy
import enum
import logging
import multiprocessing
import sys
import typing

import pydm
import pydm.data_plugins


@enum.unique
class LogLevel(int, enum.Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class PyDMApp(pydm.PyDMApplication):
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

    def new_pydm_process(self, ui_file, macros=None, command_line_args=None):
        kwargs = copy.deepcopy(
            {
                "displayfile": ui_file,
                "macros": macros,
                "hide_nav_bar": self.hide_nav_bar,
                "hide_menu_bar": self.hide_menu_bar,
                "hide_status_bar": self.hide_status_bar,
                "fullscreen": self.fullscreen,
                "read_only": pydm.data_plugins.is_read_only(),
                "perfmon": self.perfmon,
                "log_level": LogLevel.INFO,
            }
        )

        process = multiprocessing.Process(
            target=launch_pydm,
            kwargs=kwargs,
            args=command_line_args if command_line_args else [],
            daemon=False,
        )
        process.start()


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
):
    _display_args = list(display_args)
    if not macros:
        macros = {}

    logger = logging.getLogger("")
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s %(levelname)-8s %(filename)s:%(lineno)s - %(funcName)s] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel("INFO")
    handler.setLevel("INFO")

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

    logger.setLevel(log_level)
    handler.setLevel(log_level)

    app = PyDMApp(
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
    from siriushlacon.utils.images import CNPEM_INVISIBLE_LOGO_ICON

    app.setWindowIcon(CNPEM_INVISIBLE_LOGO_ICON)
    sys.exit(app.exec_())
