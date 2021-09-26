from __future__ import annotations

import os
import time
import re
from importlib import util

from shared.infrastructure.dependency_injection.container import create_container
from shared.infrastructure.environment.settings import settings
from shared.infrastructure.logging.file.logger import FileLogger
from shared.infrastructure.error.api import *


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
                mapper.map_entities()

                self.logger.info("Database tables mappings generated")
            except (ModuleNotFoundError, AttributeError):
                continue

        return self


class Application:
    _container = None

    @classmethod
    def container(cls):
        if not cls._container:
            cls._container = create_container(settings)

        return cls._container


class Utils:
    @classmethod
    def class_fullname(cls, obj: object) -> str:
        _class = obj.__class__
        module = _class.__module__
        name = _class.__qualname__
        if module is not None and module != "__builtin__":
            name = f"{module}.{name}"

        return name

    @classmethod
    def camel_case_to_snake(cls, camel_case_string: str) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_case_string).lower()
