from typing import Optional
from shared_context.infrastructure.persistence.sqlalchemy import Repository
from corpus.etl.domain.model.etl import EtlRepository, Etl, EtlId

from shared import settings


class EtlRepositoryImpl(EtlRepository, Repository):
    def __init__(self):
        super().__init__(Etl, settings.database_dsn("corpus"))

    def etl_of_tenant_and_id(self, tenant_id: str, etl_id: EtlId) -> Optional[Etl]:
        return self.find(_tenant_id=tenant_id, _etl_id=etl_id)
