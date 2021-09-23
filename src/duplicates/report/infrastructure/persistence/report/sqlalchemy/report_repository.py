from shared import settings
from shared.infrastructure.persistence.sqlalchemy.repository import Repository
from duplicates.report.domain.model.report import ReportRepository, Report


class ReportRepositoryImpl(ReportRepository, Repository):
    def __init__(self):
        super().__init__(Report, settings.database_dsn("duplicates"))
