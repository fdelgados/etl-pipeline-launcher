from __future__ import annotations

import os
import time
from importlib import util

from shared import settings
from shared.infrastructure.logging.file.logger import FileLogger
from shared.infrastructure.messaging.rabbitmq.connector import RabbitMqConnector
from bin.run_workers import consume


class Bootstrap:
    def __init__(self):
        self.logger = FileLogger()

        os.environ['TZ'] = settings.time_zone()
        time.tzset()

    def generate_db_maps(self) -> Bootstrap:
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

                self.logger.info('Database tables mappings generated')
            except (ModuleNotFoundError, AttributeError):
                continue

        return self

    def run_workers(self):
        connector = RabbitMqConnector(self.logger)
        connection = connector.connect()
        connection_channel = connection.channel()

        exchanges = settings.subscribed_events()

        for subscribed_exchange, listening_routing_keys in exchanges.items():
            consume(subscribed_exchange, listening_routing_keys, self.logger, connection_channel)
