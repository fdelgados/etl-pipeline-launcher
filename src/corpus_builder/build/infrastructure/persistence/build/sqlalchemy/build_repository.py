from typing import Optional

from shared import settings
from shared.infrastructure.persistence.sqlalchemy.repository import Repository

from corpus_builder.build.domain.model.build import BuildRepository, Build, BuildId


class BuildRepositoryImpl(BuildRepository, Repository):
    def __init__(self):
        super().__init__(Build, settings.database_dsn("corpus_builder"))

    def build_of_tenant_and_id(
        self, tenant_id: str, build_id: BuildId
    ) -> Optional[Build]:
        return self.find(_tenant_id=tenant_id, _build_id=build_id)
