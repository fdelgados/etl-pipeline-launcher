from launcher.pipeline.domain.model.page import (
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

    def find_fully_indexable(self):
        pass

    def _hydrate_all(self, results) -> List[Page]:
        return [_hydrate(result) for result in results]


    def _hydrate(self, result) -> Page:
        page = Page(
            result['ADDRESS'],
            result['STATUS_CODE'],
            result['STATUS'],
            result['LAST_EXTRACTED_ON']
        )

        page.h1 = result['H1']
        page.title = result['TITLE']
        page.content = json.loads(result['CONTENT']) if result['CONTENT'] else None
        page.canonical_address = result['CANONICAL_ADDRESS']
        page.is_indexable = bool(result['IS_INDEXABLE']) if int(result['IS_INDEXABLE']) is not None else None
        page.final_address = result['FINAL_ADDRESS']
        page.datalayer = json.loads(result['DATALAYER']) if result['DATALAYER'] else None

        return page
