import logging
import multiprocessing
import shlex
import subprocess
import sys
import threading
import typing

from qtpy.QtWidgets import QMainWindow, QWidget

from siriushlacon.utils import close_qt_application

_logger = logging.getLogger(__name__)


class CommandRunner:
    def __init__(
        self,
        command: typing.Callable[[], typing.Any],
        name: typing.Optional[str] = None,
        close_when_finished: bool = False,
        parent_widget: typing.Optional[QWidget] = None,
    ):
        if not command:
            raise RuntimeError("command argument cannot be empty")

        if parent_widget:
            if isinstance(parent_widget, QMainWindow):
                parent_widget = None
                _logger.warning(
                    f"parameter 'parent_widget' {parent_widget} is a {QMainWindow}, arument 'close_when_finished' will terminate the application"
                )
            elif not isinstance(parent_widget, QWidget):
                raise TypeError(
                    f"parameter 'parent_widget' must be of type {QWidget}, received {parent_widget}"
                )
        if not parent_widget and close_when_finished:
            _logger.warning(
                f"{self} does not have a parent widget, qt app will be closed"
            )

        self._parent_widget: typing.Optional[QWidget] = parent_widget
        self._close_when_finished = close_when_finished
        self._command = command
        self._name = name
        self._thread: typing.Optional[
            typing.Union[threading.Thread, multiprocessing.Process]
        ] = None

    def _command_log(self):
        self._command()
        _logger.info(f"Thread finished {self._thread}")
        if self._close_when_finished:
            if self._parent_widget:
                _logger.info(
                    f"qt widget {self._parent_widget} being closed from {self._thread}"
                )
                self._parent_widget.close()
            else:
                _logger.info(f"qt appliacation being closed from {self._thread}")
                close_qt_application()

    def _create_thread(self):
        self._thread = threading.Thread(target=self._command_log, daemon=False)
        if self._name:
            self._thread.name = self._name
        _logger.info(f"Thread {self._thread!r} created")

    def execute_command(
        self, join: bool = False, timeout: typing.Optional[float] = None
    ):
        if self._thread and self._thread.is_alive():
            _logger.error(f"Cannot start thread, {self._thread!r} is alive")
            return

        self._create_thread()
        if not self._thread:
            raise RuntimeError("Failed to create thread")

        self._thread.start()
        _logger.info(f"Thread stated {self._thread!r} join={join}")
        if join:
            self._thread.join(timeout=timeout)


class ShellCommandRunner:
    def __init__(self, command: str):
        self.command = command
        self.process: typing.Optional[subprocess.Popen] = None

    def execute_command(self):
        if not self.command:
            _logger.info("The command is not set, so no command was executed.")
            return

        if self.process is None or self.process.poll() is not None:
            args = shlex.split(self.command, posix="win" not in sys.platform)
            try:
                _logger.info(f"Launching process: {repr(args)}")
                self.process = subprocess.Popen(args)
            except Exception:
                _logger.exception(f"Error in shell command: {self.command}")
        else:
            _logger.error(f"Command {self.command!r} already active.")
