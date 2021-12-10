from typing import Optional

import shared.infrastructure.environment.globalvars as global_vars
from shared.infrastructure.persistence.sqlalchemy.repository import Repository
from duplicates.report.domain.model.report import (
    ReportRepository,
    Report,
    ReportId,
    Status,
)


class ReportRepositoryImpl(ReportRepository, Repository):
    def __init__(self):
        super().__init__(
            Report, global_vars.settings.database_dsn("duplicates")
        )

    def report_of_id(self, report_id: ReportId) -> Optional[Report]:
        return self.find(_report_id=report_id)

    def last_of_tenant(self, tenant_id: str) -> Report:
        session = self._session()
        query = (
            session.query(self._aggregate)
            .filter(Report._tenant_id == tenant_id,
                    Report._status == Status.completed())
            .order_by(Report._completed_on.desc())
        )

        result = query.first()

        session.close()
        self._engine.dispose()

        return result
