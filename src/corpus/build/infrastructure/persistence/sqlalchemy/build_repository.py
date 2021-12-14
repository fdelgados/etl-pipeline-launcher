from typing import Optional, List

import shared.infrastructure.environment.globalvars as global_vars

from shared.infrastructure.persistence.sqlalchemy.repository import Repository

from corpus.build.domain.model.build import (
    BuildRepository,
    Build,
    BuildId,
    Status,
)


class BuildRepositoryImpl(BuildRepository, Repository):
    def __init__(self):
        super().__init__(Build, global_vars.settings.database_dsn("corpus"))

    def builds_of_tenant(self, tenant_id: str) -> List[Build]:
        session = self._session()
        query = (
            session.query(self._aggregate)
            .filter_by(_tenant_id=tenant_id)
            .order_by(Build._started_on.desc())
        )

        result = query.all()

        session.close()
        self._engine.dispose()

        return result

    def running_builds_of_tenant(self, tenant_id: str) -> List[Build]:
        return self.find_all(_tenant_id=tenant_id, _status=Status.running())

    def build_of_tenant_and_id(
        self, tenant_id: str, build_id: BuildId
    ) -> Optional[Build]:
        return self.find(_tenant_id=tenant_id, _build_id=build_id)
