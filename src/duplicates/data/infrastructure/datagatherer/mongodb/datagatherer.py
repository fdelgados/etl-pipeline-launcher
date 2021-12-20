from pymongo import MongoClient

from typing import List

import shared.infrastructure.environment.globalvars as global_vars

from shared.domain.model.valueobject.url import Url

from duplicates.data.domain.model.page import Page
from duplicates.data.domain.service.datagatherer import DataGatherer


def _add_pages(documents: list, pages: List[Page]) -> None:
    for document in documents:
        content = [section for _, section in document.get("content").items()]

        pages.append(
            Page(
                Url(document.get("address")),
                " ".join(content),
                document.get("datalayer"),
            )
        )


class DataGathererImpl(DataGatherer):
    _PAGE_SIZE = 1000

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
        pages = []
        last_id = None

        while True:
            documents, last_id = self._retrieve_documents(
                corpus,
                corpus_build_id,
                last_id,
            )

            if documents is None and last_id is None:
                break

            _add_pages(documents, pages)

        return pages

    def _retrieve_documents(
        self,
        corpus: str,
        corpus_build_id: str,
        last_id=None,
    ):
        pages_collection = self._client[self._database][corpus]

        query = {
            "is_indexable": {"$eq": True},
            "status_code": {"$eq": 200},
            "build_id": {"$eq": corpus_build_id},
        }

        if last_id is not None:
            query["_id"] = {"$gt": last_id}

        cursor = pages_collection.find(
            query,
            {
                "address": 1,
                "content": 1,
                "datalayer": 1,
            },
        ).limit(self._PAGE_SIZE)

        documents = [document for document in cursor]

        if not documents:
            return None, None

        last_id = documents[-1]["_id"]

        return documents, last_id
