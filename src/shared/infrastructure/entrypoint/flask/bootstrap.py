from importlib import util

from shared import settings
from shared.infrastructure.logging.file.logger import FileLogger
from shared.infrastructure.messaging.rabbitmq.connector import RabbitMqConnector


class Bootstrap:
    def __init__(self):
        self.logger = FileLogger()
        self._app = None
        self._api = None

        self._generate_db_maps()
        self._setup_messages_queues()

    def _generate_db_maps(self) -> None:
        self.logger.info('Generating database tables mappings')
        for mapping_class in settings.db_mapping_classes():
            module_name, class_name = mapping_class.rsplit('.', 1)

            try:
                spec = util.find_spec(module_name)
                module = util.module_from_spec(spec)
                spec.loader.exec_module(module)

                class_ = getattr(module, class_name)
                mapper = class_()
                mapper.start_mappers()
            except (ModuleNotFoundError, AttributeError):
                continue

    def _setup_messages_queues(self) -> None:
        self.logger.info('Setup message broker')

        connector = RabbitMqConnector(self.logger)
        connection = connector.connect()

        exchanges = settings.rabbit_exchanges()

        try:
            channel = connection.channel()

            for exchange_name, queues in exchanges.items():
                channel.exchange_declare(exchange=exchange_name, exchange_type='fanout', durable=True)
                for queue in queues:
                    queue_name = list(queue.values())[0]
                    channel.queue_declare(queue_name, durable=True)
                    channel.queue_bind(queue_name, exchange_name)
        except Exception as error:
            self.logger.error(str(error))

            raise
        finally:
            connector.disconnect()
