import json
import pika
from pika import exceptions

from shared_context.domain.events import DomainEvent
from shared import settings
from shared.domain.service.messaging.publisher import EventPublisher
from shared.domain.service.logging.logger import Logger
from .connector import RabbitMqConnector


class RabbitMqEventPublisher(EventPublisher):
    def __init__(self, logger: Logger):
        self._logger = logger
        self._connector = RabbitMqConnector(self._logger)

    def publish(self, event: DomainEvent, publisher: str) -> None:
        connection = self._connect()

        try:
            channel = connection.channel()
            channel.exchange_declare(
                exchange=publisher, exchange_type="direct", durable=True
            )
            channel.basic_publish(
                exchange=publisher,
                routing_key=event.event_name(),
                body=self._build_message(event),
                properties=pika.BasicProperties(delivery_mode=2),
            )
        except (exceptions.AMQPError, ValueError) as error:
            self._logger.error(str(error))

            raise
        finally:
            self._disconnect()

    def _build_message(self, event: DomainEvent):
        message = {
            "metadata": {"environment": settings.environment()},
            "body": json.loads(event.serialize()),
        }

        return json.dumps(message).encode()

    def _connect(self):
        return self._connector.connect()

    def _disconnect(self):
        self._connector.disconnect()
