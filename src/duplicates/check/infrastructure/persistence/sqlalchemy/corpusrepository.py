import json

from duplicates.check.domain.model.corpus import (
    Corpus,
    CorpusRepository,
)

from shared.infrastructure.persistence.sqlalchemy.dbal import DbalService


class CorpusRepositoryImpl(CorpusRepository):
    def __init__(self, db_service: DbalService):
        self._db_service = db_service

    def corpus_of_name(self, tenant_id: str, name: str) -> Corpus:
        sentence = """
            SELECT name, request_headers, selector_mapping,
                excluded_tags, excluded_selectors
            FROM corpora
            WHERE name = :name
            AND tenant_id = :tenant_id
        """

        result = self._db_service.execute(
            sentence, tenant_id=tenant_id, name=name
        )

        row = result.fetchone()

        return Corpus(
            row["name"],
            json.loads(row["request_headers"] or "{}"),
            json.loads(row["excluded_tags"] or "[]"),
            json.loads(row["excluded_selectors"] or "[]"),
            json.loads(row["selector_mapping"] or "{}"),
        )
