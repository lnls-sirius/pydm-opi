import logging
import subprocess
import sys

import typing
import shlex

logger = logging.getLogger(__name__)


class ShellCommandRunner:
    def __init__(self, command: str, allow_multiple=False):
        self.command = command
        self.process: typing.Optional[subprocess.Popen] = None
        self._allow_multiple = allow_multiple

    def execute_command(self):
        if not self.command:
            logger.info("The command is not set, so no command was executed.")
            return

        if (
            self.process is None or self.process.poll() is not None
        ) or self._allow_multiple:
            args = shlex.split(self.command, posix="win" not in sys.platform)
            try:
                logger.info(f"Launching process: {repr(args)}")
                self.process = subprocess.Popen(args)
            except Exception:
                logger.exception(f"Error in shell command: {self.command}")
        else:
            logger.error(f"Command '{self.command}' already active.")
