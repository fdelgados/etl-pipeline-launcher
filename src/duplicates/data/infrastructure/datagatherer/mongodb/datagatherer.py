from pymongo import MongoClient

from typing import List

import shared.infrastructure.environment.globalvars as global_vars

from shared.domain.model.valueobject.url import Url

from duplicates.data.domain.model.page import Page
from duplicates.data.domain.service.datagatherer import DataGatherer


class DataGathererImpl(DataGatherer):
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

    def gather(self, corpus: str, corpus_build_id: str) -> List[Page]:
        pages_collection = self._client[self._database][corpus]
        pages = []

        documents = pages_collection.find(
            {
                "is_indexable": {"$eq": True},
                "status_code": {"$eq": 200},
                "build_id": corpus_build_id,
            },
            {
                "_id": 0,
                "address": 1,
                "content": 1,
            },
        )

        for document in documents:
            content = [
                section for _, section in document.get("content").items()
            ]
            pages.append(
                Page(
                    Url(document.get("address")),
                    " ".join(content),
                    document.get("datalayer"),
                )
            )

        return pages
