from typing import Optional, List

import shared.infrastructure.environment.globalvars as glob

from shared.infrastructure.persistence.sqlalchemy.repository import Repository

from corpus.build.domain.model.build import (
    BuildRepository,
    Build,
    BuildId,
    Status,
)


class BuildRepositoryImpl(BuildRepository, Repository):
    def __init__(self):
        super().__init__(Build, glob.settings.database_dsn("corpus"))

    def builds_of_tenant(self, tenant_id: str) -> List[Build]:
        return self.find_all(
            order_by={"_started_on": "desc"}, _tenant_id=tenant_id
        )

    def running_builds_of_tenant(self, tenant_id: str) -> List[Build]:
        return self.find_all(_tenant_id=tenant_id, _status=Status.running())

    def build_of_tenant_and_id(
        self, tenant_id: str, build_id: BuildId
    ) -> Optional[Build]:
        return self.find(_tenant_id=tenant_id, _build_id=build_id)
