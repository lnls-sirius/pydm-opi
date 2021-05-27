import logging
import shlex
import subprocess
import sys
import threading
import typing

logger = logging.getLogger(__name__)


class CommandRunner:
    def __init__(
        self,
        command: typing.Callable[[], typing.Any],
        name: typing.Optional[str] = None,
    ):
        if not command:
            raise RuntimeError("command argument cannot be empty")

        self._command = command
        self._name = name
        self._thread: typing.Optional[threading.Thread] = None

    def _command_log(self):
        self._command()
        logger.info(f"Thread finished {self._thread}")

    def _create_thread(self):
        self._thread = threading.Thread(target=self._command_log, daemon=False)
        if self._name:
            self._thread.name = self._name
        logger.info(f"Thread '{self._thread}' created")

    def execute_command(
        self, join: bool = False, timeout: typing.Optional[float] = None
    ):
        if self._thread and self._thread.is_alive():
            logger.error(f"Cannot start thread, '{self._thread}' is alive")
            return

        self._create_thread()
        if not self._thread:
            raise RuntimeError("Failed to create thread")

        self._thread.start()
        logger.info(f"Thread stated '{self._thread}' join={join}")
        if join:
            self._thread.join(timeout=timeout)


class ShellCommandRunner:
    def __init__(self, command: str):
        self.command = command
        self.process: typing.Optional[subprocess.Popen] = None

    def execute_command(self):
        if not self.command:
            logger.info("The command is not set, so no command was executed.")
            return

        if self.process is None or self.process.poll() is not None:
            args = shlex.split(self.command, posix="win" not in sys.platform)
            try:
                logger.info(f"Launching process: {repr(args)}")
                self.process = subprocess.Popen(args)
            except Exception:
                logger.exception(f"Error in shell command: {self.command}")
        else:
            logger.error(f"Command '{self.command}' already active.")
