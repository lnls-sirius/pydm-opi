import logging as _logging
import typing as _typing

_formatter = _logging.Formatter(
    "[%(asctime)s %(levelname)s %(filename)s:%(lineno)s - %(funcName)s] %(message)s"
)
_console_handler = _logging.StreamHandler()
_console_handler.setFormatter(_formatter)


def get_logger(
    name=__file__,
    level: int = _logging.INFO,
    handlers: _typing.Optional[_typing.List[_logging.Handler]] = None,
) -> _logging.Logger:
    """Returns a logger object"""

    logger = _logging.getLogger(name)

    if not handlers:
        logger.setLevel(level)
        logger.addHandler(_console_handler)
    return logger
