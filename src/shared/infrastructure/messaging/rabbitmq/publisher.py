from pika import exceptions

from shared.domain.service.messaging.publisher import Publisher
from shared.domain.service.logging.logger import Logger
from .connector import RabbitMqConnector


class RabbitMqPublisher(Publisher):
    def __init__(self, logger: Logger):
        self._logger = logger
        self._connector = RabbitMqConnector(self._logger)

    def publish(self, message: str, exchange: str = '') -> None:
        connection = self._connect()

        try:
            channel = connection.channel()
            channel.basic_publish(exchange=exchange, routing_key='', body=message.encode())
        except (exceptions.AMQPError, ValueError) as error:
            self._logger.error(str(error))

            raise
        finally:
            self._disconnect()

    def _connect(self):
        return self._connector.connect()

    def _disconnect(self):
        self._connector.disconnect()
