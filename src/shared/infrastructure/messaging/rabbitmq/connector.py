from typing import Optional, Dict
import pika
from pika import exceptions
import shared.infrastructure.environment.globalvars as global_vars
from shared.domain.service.logging.logger import Logger


class RabbitMqConnector:
    def __init__(self, logger: Logger):
        self._logger = logger
        self._connection = None

    def connect(
        self, connect_settings: Optional[Dict] = None
    ) -> pika.BlockingConnection:

        if not connect_settings:
            connect_settings = (
                global_vars.settings.rabbit_connection_settings()
            )

        credentials = pika.PlainCredentials(
            connect_settings.get("user"),
            connect_settings.get("password"),
        )

        try:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=connect_settings.get("host"),
                    port=connect_settings.get("port"),
                    virtual_host=connect_settings.get("vhost", "/"),
                    credentials=credentials,
                )
            )

            return self._connection
        except Exception as error:
            self._logger.error(repr(error))

            raise Exception(repr(error))

    def disconnect(self):
        if not self._connection:
            return

        try:
            self._connection.close()
        except exceptions.ConnectionWrongStateError as error:
            self._logger.warning(str(error))
