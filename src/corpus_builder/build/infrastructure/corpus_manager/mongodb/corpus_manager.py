from pymongo import MongoClient

import shared.infrastructure.environment.global_vars as glob
from corpus_builder.build.domain.service.corpus_manager import CorpusManager


class CorpusManagerImpl(CorpusManager):
    def __init__(self, database: str):
        databases = glob.settings.mongodb_databases()
        connection_settings = glob.settings.mongodb_connection_settings()

        self._database = databases.get(database)
        self._client = MongoClient(
            connection_settings.get("host"),
            port=connection_settings.get("port"),
            username=connection_settings.get("username"),
            password=connection_settings.get("password"),
            authSource=self._database,
            connect=False,
        )

    def rotate(self, corpus: str) -> None:
        tmp_collection = self._client[self._database][f"{corpus}_tmp"]
        tmp_collection.rename(corpus.replace("_tmp", ""), dropTarget=True)

    def clean(self, corpus: str) -> None:
        tmp_collection = self._client[self._database][f"{corpus}_tmp"]
        tmp_collection.drop()
