import abc

from typing import List, Optional

from pymongo import MongoClient

from shared.domain.model.aggregate import AggregateRoot
from shared.domain.model.repository import Repository
import shared.infrastructure.environment.globalvars as global_vars


class MongoDbRepository(Repository, metaclass=abc.ABCMeta):
    def __init__(self):
        connect_settings = global_vars.settings.mongodb_connection_settings()

        self._database = connect_settings.get("database")
        self._client = MongoClient(
            connect_settings.get("host"),
            port=connect_settings.get("port"),
            username=connect_settings.get("username"),
            password=connect_settings.get("password"),
            authSource=connect_settings.get("database"),
            connect=False,
        )

    @property
    def client(self) -> MongoClient:
        return self._client

    @property
    def database(self):
        return self.client[self._database]

    def add(self, aggregate: AggregateRoot) -> None:
        pass

    def save(self, aggregate: AggregateRoot) -> None:
        pass

    def find(self, **kwargs) -> Optional[AggregateRoot]:
        pass

    def find_all(self, **kwargs) -> List[AggregateRoot]:
        pass
