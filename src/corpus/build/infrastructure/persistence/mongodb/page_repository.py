from typing import List
from pymongo import errors

from corpus.build.domain.model.page import (
    PageRepository,
    Page,
    UnableToSavePageError,
)

from shared.infrastructure.persistence.mongodb.repository import MongoDbRepository


class MongoDbPageRepository(PageRepository, MongoDbRepository):
    def __init__(self, database: str):
        super().__init__(database)

        self._collection = None

    def save(self, page: Page) -> None:
        tmp_collection = self.database[f"{page.corpus_name}_tmp"]
        tmp_collection.create_index("address", unique=True)

        try:
            tmp_collection.update_one(
                {"address": page.url.address},
                {
                    "$set": {
                        "corpus": page.corpus_name,
                        "document_type": page.type,
                        "tenant_id": page.tenant_id,
                        "address": page.url.address,
                        "status": page.status,
                        "status_code": page.status_code,
                        "h1": page.h1,
                        "title": page.title,
                        "content": page.content,
                        "is_indexable": page.is_indexable,
                        "final_address": None
                        if not page.final_url
                        else page.final_url.address,
                        "canonical_address": None
                        if not page.canonical_url
                        else page.canonical_url.address,
                        "datalayer": page.datalayer,
                        "modified_on": page.modified_on,
                    }
                },
                upsert=True,
            )
        except errors.PyMongoError as error:
            raise UnableToSavePageError(
                f"Cannot save page content ({page.url.address}). {str(error)}"
            )

    def add(self, page: Page) -> None:
        pass

    def find(self, **kwargs) -> Page:
        pass

    def find_all(self, **kwargs) -> List[Page]:
        pass
