import tqdm
import sys
import logging

from typing import Optional

from shared import settings
from shared.domain.service.logging.logger import Logger


class TqdmLoggingHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.tqdm.write(msg)
            self.flush()
        except Exception:
            self.handleError(record)


class ProgressBarLogger(Logger):
    def __init__(self, name: str = 'application'):
        self._name = name
        logger = self._logger

        level = logging.DEBUG
        if settings.is_production():
            level = logging.WARNING

        logger.setLevel(level)
        logger.addHandler(TqdmLoggingHandler())

    @property
    def _logger(self):
        return logging.getLogger(self._name)

    def debug(self, message: str, *args) -> None:
        pass

    def info(self, message: str, *args) -> None:
        pass

    def warning(self, message: str, *args) -> None:
        pass

    def error(self, message: str, *args) -> None:
        pass

    def critical(self, message: str) -> None:
        pass

    file = None

    def write(self, x):
        # Avoid print() second call (useless \n)
        if len(x.rstrip()) > 0:
            tqdm.tqdm.write(x, file=self.file, end='')

    def flush(self):
        return getattr(self.file, "flush", lambda: None)()
