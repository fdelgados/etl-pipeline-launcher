import logging
import traceback
import sys

from typing import Optional

from shared import settings
from shared.domain.service.logging.logger import Logger


class FileLogger(Logger):
    def __init__(self, name: str = 'application', logfile: Optional[str] = None):
        self._name = name
        logger = self._logger

        if not logfile:
            logfile = name

        level = logging.DEBUG
        if settings.is_production():
            level = logging.WARNING

        logger.setLevel(level)

        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        file_handler = logging.FileHandler(f'{settings.logs_dir()}/{logfile}.log')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    @property
    def _logger(self):
        return logging.getLogger(self._name)

    def debug(self, message: str, *args) -> None:
        self._logger.debug(message, *args)

    def info(self, message: str, *args) -> None:
        self._logger.info(message, *args)

    def warning(self, message: str, *args) -> None:
        self._logger.warning(self._format_message(message), *args)

    def error(self, message: str, *args) -> None:
        self._logger.error(self._format_message(message), *args)

    def critical(self, message: str, *args) -> None:
        self._logger.critical(self._format_message(message), *args)

    def _format_message(self, message: str):
        exc_type, exc_value, exc_tb = sys.exc_info()

        if not exc_type and not exc_value and not exc_tb:
            return message

        tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
        stack = tb.stack[0]

        return f'{message}. File {stack.filename}, line {stack.lineno} in <{stack.name}>'

