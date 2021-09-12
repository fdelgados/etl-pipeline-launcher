from pydic import create_container
from .infrastructure.environment.settings import settings
from .infrastructure.error.api import *


class Application:
    _container = None

    @classmethod
    def container(cls):
        if not cls._container:
            cls._container = create_container(
                settings.services_files(), settings.event_handlers_file()
            )

        return cls._container
