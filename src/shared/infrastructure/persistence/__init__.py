import abc
from typing import List, Optional

from pymongo import MongoClient

from shared import settings
from shared_context.domain.model import Repository, AggregateRoot


class MongoDbRepository(Repository, metaclass=abc.ABCMeta):
    def __init__(
        self,
        database: str,
        collection: str,
        username: str,
        password: str,
        host: Optional[str] = 'localhost',
        port: Optional[int] = 27017
    ):
        self._client = MongoClient(
            host=host,
            port=port,
            username=username,
            password=password,
            authSource=database
        )
        self._collection = collection

    @property
    def client(self) -> MongoClient:
        return self._client

    @property
    def database(self):
        return self.client.get_database()

    @property
    def collection(self):
        database = self.database

        return database[self._collection]

    def add(self, aggregate: AggregateRoot) -> None:
        pass

    def save(self, aggregate: AggregateRoot) -> None:
        pass

    def find(self, **kwargs) -> AggregateRoot:
        pass

    def find_all(self, **kwargs) -> List[AggregateRoot]:
        pass


class BaseMongoDbRepository(MongoDbRepository, metaclass=abc.ABCMeta):
    def __init__(self, database: str, collection: str):
        connection_settings = settings.mongodb_connection_settings()
        databases = settings.mongodb_databases()

        super().__init__(
            databases.get(database),
            collection,
            connection_settings.get('username'),
            connection_settings.get('password'),
            host=connection_settings.get('host'),
            port=connection_settings.get('port')
        )
