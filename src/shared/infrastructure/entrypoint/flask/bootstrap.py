from __future__ import annotations

import os
import time
from importlib import util

from shared import settings
from shared.infrastructure.logging.file.logger import FileLogger


class Bootstrap:
    def __init__(self):
        self.logger = FileLogger()

        os.environ["TZ"] = settings.time_zone()
        time.tzset()

    def generate_db_maps(self) -> Bootstrap:
        self.logger.info("Generating database tables mappings")
        for mapping_class in settings.db_mapping_classes():
            module_name, class_name = mapping_class.rsplit(".", 1)

            try:
                spec = util.find_spec(module_name)
                module = util.module_from_spec(spec)
                spec.loader.exec_module(module)

                class_ = getattr(module, class_name)
                mapper = class_()
                mapper.start_mappers()

                self.logger.info("Database tables mappings generated")
            except (ModuleNotFoundError, AttributeError):
                continue

        return self
