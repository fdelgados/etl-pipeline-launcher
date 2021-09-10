from corpus.etl.domain.model.page import (
    PageRepository,
    Page
)

from shared.infrastructure.persistence.mongodb.repository import BaseMongoDbRepository


class MongoDbPageRepository(PageRepository, BaseMongoDbRepository):
    def save(self, page: Page) -> None:
        self.collection.update_one(
            {
                'address': page.url.address
            },
            {
                '$set': {
                    'status': page.status,
                    'status_code': page.status_code,
                    'h1': page.h1,
                    'title': page.title,
                    'content': page.content,
                    'is_indexable': page.is_indexable,
                    'final_address': None if not page.final_url else page.final_url.address,
                    'canonical_address': None if not page.canonical_url else page.canonical_url.address,
                    'datalayer': page.datalayer,
                    'modified_on': page.modified_on
                }
            },
            upsert=True
        )
