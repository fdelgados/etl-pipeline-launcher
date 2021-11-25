from pymongo import MongoClient

import shared.infrastructure.environment.globalvars as glob
from corpus.build.domain.service.corpus_manager import CorpusManager


class CorpusManagerImpl(CorpusManager):
    def __init__(self):
        connection_settings = glob.settings.mongodb_connection_settings()

        self._database = connection_settings.get("database")
        self._client = MongoClient(
            connection_settings.get("host"),
            port=connection_settings.get("port"),
            username=connection_settings.get("username"),
            password=connection_settings.get("password"),
            authSource=connection_settings.get("database"),
            connect=False,
        )

    def rotate(self, corpus: str) -> None:
        tmp_collection = self._client[self._database][f"{corpus}_tmp"]
        tmp_collection.rename(corpus.replace("_tmp", ""), dropTarget=True)

    def clean(self, corpus: str) -> None:
        tmp_collection = self._client[self._database][f"{corpus}_tmp"]
        tmp_collection.drop()
