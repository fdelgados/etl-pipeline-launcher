import abc

from typing import List

from shared_context.domain.model import AggregateRoot
from shared_context.infrastructure.persistence.mongodb import MongoDbRepository
from shared import settings


class BaseMongoDbRepository(MongoDbRepository, metaclass=abc.ABCMeta):
    def __init__(self, database: str):
        connection_settings = settings.mongodb_connection_settings()
        databases = settings.mongodb_databases()

        super().__init__(
            databases.get(database),
            connection_settings.get("username"),
            connection_settings.get("password"),
            host=connection_settings.get("host"),
            port=connection_settings.get("port"),
        )

    def save(self, aggregate: AggregateRoot) -> None:
        pass

    def add(self, aggregate: AggregateRoot) -> None:
        pass

    def find(self, **kwargs) -> AggregateRoot:
        pass

    def find_all(self, **kwargs) -> List[AggregateRoot]:
        pass
