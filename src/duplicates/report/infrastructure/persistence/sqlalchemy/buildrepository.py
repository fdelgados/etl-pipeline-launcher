import uuid

from shared.infrastructure.persistence.sqlalchemy.dbal import DbalService
from duplicates.report.domain.model.build import Build, BuildRepository


class BuildRepositoryImpl(BuildRepository):
    def __init__(self, db_service: DbalService):
        self._db_service = db_service

    def last_build(self, tenant_id: str, corpus_name: str) -> Build:
        sentence = """
            SELECT id, name, started_on
            FROM builds 
            WHERE tenant_id = :tenant_id
            AND status = 1
            AND corpus_name = :corpus_name
            ORDER BY started_on DESC
            LIMIT 1
        """

        result = self._db_service.execute(
            sentence,
            tenant_id=tenant_id,
            corpus_name=corpus_name
        )

        row = result.fetchone()

        return Build(
            str(uuid.UUID(bytes=row["id"])),
            row["name"],
            row["started_on"]
        )
