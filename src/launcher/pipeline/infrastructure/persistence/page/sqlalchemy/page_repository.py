import json
from sqlalchemy import text
from shared import settings
from shared_context.infrastructure.persistence.sqlalchemy import Repository
from launcher.pipeline.domain.model.document import (
    PageRepository,
    Page
)


class PageRepositoryImpl(PageRepository, Repository):
    def __init__(self):
        super().__init__(Page, settings.database_dsn('launcher'))

    def save(self, page: Page) -> None:
        connection = self.create_connection()
        sentence = '''INSERT INTO web_corpus (
                                address,
                                status_code,
                                status,
                                h1,
                                title,
                                content,
                                is_indexable,
                                final_address,
                                canonical_address,
                                datalayer,
                                modified_on
                            )
                        VALUES (:address, :status_code, :status, :h1, :title,
                                :content, :is_indexable, :final_address, :canonical_address,
                                :datalayer, :modified_on)
                        ON DUPLICATE KEY UPDATE
                            status_code = :status_code,
                            status = :status,
                            h1 = :h1,
                            title = :title,
                            content = :content,
                            is_indexable = :is_indexable,
                            final_address = :final_address,
                            canonical_address = :canonical_address,
                            datalayer = :datalayer,
                            modified_on = :modified_on'''
        with connection.connect() as conn:
            try:
                conn.execute(
                    text(sentence),
                    address=page.url.address,
                    status_code=page.status_code,
                    status=page.status,
                    h1=page.h1,
                    title=page.title,
                    content=json.dumps(page.content, ensure_ascii=False),
                    is_indexable=page.is_indexable,
                    final_address=None if not page.final_url else page.final_url.address,
                    canonical_address=None if not page.canonical_url else page.canonical_url.address,
                    datalayer=json.dumps(page.datalayer, ensure_ascii=False),
                    modified_on=page.modified_on
                )
            except Exception as error:
                raise Exception(f'{page.url.address}: {str(error)}')
