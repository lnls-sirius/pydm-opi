import logging
import subprocess
import sys
import threading

import typing
import shlex

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

    def _create_thread(self):
        self._thread = threading.Thread(target=self.command, daemon=False)
        if self.name:
            self._thread.name = self.name
        logger.info(f"Thread '{self._thread}' created")

    def execute_command(self, join: bool, timeout: typing.Optional[float]):
        if self._thread and self._thread.is_alive():
            logger.error(f"Cannot start thread, '{self._thread}' is alive")
            return

        self._create_thread()
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
