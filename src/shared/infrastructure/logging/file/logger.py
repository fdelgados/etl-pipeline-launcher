import os
import logging

from typing import Optional

from shared.infrastructure.environment.settings import Settings
from shared.domain.service.logging.logger import Logger


class FileLogger(Logger):
    def __init__(
        self, name: Optional[str] = None, logfile: Optional[str] = None
    ):
        self._settings = Settings.common_settings()
        if not name:
            name = "application"

        self._name = name
        logger = self._logger

        if not logfile:
            logfile = self._name

        logger.setLevel(self.level())

        formatter = logging.Formatter(
            "%(asctime)s :: %(levelname)s :: %(message)s"
        )

        logs_dir = self._logs_dir()

        file = f"{logs_dir}/{logfile}.log"
        if not os.path.isfile(file):
            open(file, "w")

        file_handler = logging.FileHandler(file)
        logging.StreamHandler()
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    def _logs_dir(self) -> str:
        return self._settings.get("application").get("logs_dir")

    def level(self) -> int:
        level = logging.DEBUG

        if os.environ.get("ENVIRONMENT", "development") == "production":
            level = logging.WARNING

        return level

    @property
    def _logger(self):
        return logging.getLogger(self._name)

    def debug(self, message: str, *args) -> None:
        self._logger.debug(message, *args)

    def info(self, message: str, *args) -> None:
        self._logger.info(message, *args)

    def warning(self, message: str, *args) -> None:
        self._logger.warning(message, *args)

    def error(self, message: str, *args) -> None:
        self._logger.error(message, *args)

    def critical(self, message: str, *args) -> None:
        self._logger.critical(message, *args)
