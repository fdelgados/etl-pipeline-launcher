from shared_context.infrastructure.persistence.sqlalchemy import Repository
from duplicates.report.domain.model.report import ReportRepository, Report

from shared import settings


class ReportRepositoryImpl(ReportRepository, Repository):
    def __init__(self):
        super().__init__(Report, settings.database_dsn("duplicates"))
