import shared.infrastructure.environment.global_vars as glob
from shared.infrastructure.persistence.sqlalchemy.repository import Repository
from duplicates.report.domain.model.report import ReportRepository, Report


class ReportRepositoryImpl(ReportRepository, Repository):
    def __init__(self):
        super().__init__(Report, glob.settings.database_dsn("duplicates"))
