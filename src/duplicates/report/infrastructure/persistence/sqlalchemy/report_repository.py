from typing import Optional

import shared.infrastructure.environment.globalvars as global_vars
from shared.infrastructure.persistence.sqlalchemy.repository import Repository
from duplicates.report.domain.model.report import (
    ReportRepository,
    Report,
    ReportId,
)


class ReportRepositoryImpl(ReportRepository, Repository):
    def __init__(self):
        super().__init__(
            Report,
            global_vars.settings.database_dsn("duplicates")
        )

    def report_of_id(self, report_id: ReportId) -> Optional[Report]:
        return self.find(_report_id=report_id)
