import re
from .infrastructure.dependency_injection.container import create_container
from .infrastructure.environment.settings import settings
from .infrastructure.error.api import *


class Application:
    _container = None

    @classmethod
    def container(cls):
        if not cls._container:
            cls._container = create_container(
                settings.services_files(), settings.event_handlers_files()
            )

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
