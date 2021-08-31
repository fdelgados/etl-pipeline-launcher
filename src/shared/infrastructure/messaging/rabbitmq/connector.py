import pika
from pika import exceptions
from shared import settings
from shared.domain.service.logging.logger import Logger


class RabbitMqConnector:
    def __init__(self, logger: Logger):
        self._logger = logger
        self._connection = None

    def connect(self) -> pika.BlockingConnection:
        connection_settings = settings.rabbit_connection_settings()
        credentials = pika.PlainCredentials(
            connection_settings.get('user'),
            connection_settings.get('password')
        )

        try:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=connection_settings.get('host'),
                    port=connection_settings.get('port'),
                    virtual_host='/',
                    credentials=credentials
                )
            )

            return self._connection
        except exceptions.AMQPConnectionError as error:
            self._logger.error(str(error))

            raise

    def disconnect(self):
        try:
            self._connection.close()
        except exceptions.ConnectionWrongStateError as error:
            self._logger.warning(str(error))
