from pymongo import MongoClient

from typing import List

import shared.infrastructure.environment.global_vars as glob

from shared.domain.model.value_object.url import Url

from duplicates.data.domain.model.page import Page
from duplicates.data.domain.service.datagatherer import DataGatherer


class DataGathererImpl(DataGatherer):
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

    def gather(self, corpus: str) -> List[Page]:
        pages_collection = self._client[self._database][corpus]
        pages = []

        documents = pages_collection.find({
            "is_indexable": {"$eq": True},
            "status_code": {"$eq": 200},
            "document_type": {"$eq": "web_page"}
        })

        for document in documents:
            content = [section for _, section in document.get("content").items()]
            pages.append(
                Page(
                    Url(document.get("address")),
                    " ".join(content),
                    document.get("datalayer"),
                )
            )

        return pages
