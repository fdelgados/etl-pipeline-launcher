import shared.infrastructure.environment.globalvars as global_vars

from duplicates.report.domain.model.report import (
    DuplicateRepository,
    Duplicate,
    ReportId,
)

from shared.infrastructure.persistence.sqlalchemy.repository import Repository


class DuplicateRepositoryImpl(DuplicateRepository, Repository):
    def __init__(self):
        super().__init__(
            Duplicate, global_vars.settings.database_dsn("duplicates")
        )

    def count(self, report_id: ReportId) -> int:
        sentence = """
            SELECT COUNT(DISTINCT url) AS num_duplicates FROM report_duplicates
            WHERE report_id = :report_id
        """

        with self._connection().connect() as connection:
            result = connection.execute(
                self._statement(sentence), report_id=bytes(report_id)
            )

            duplicates = result.scalar()

            connection.close()
            self._connection().dispose()

            return duplicates

    def similarity_average(self, report_id: ReportId) -> float:
        sentence = """
            SELECT AVG(similarity) AS similarity_average FROM report_duplicates
            WHERE report_id = :report_id
        """

        with self._connection().connect() as connection:
            result = connection.execute(
                self._statement(sentence), report_id=bytes(report_id)
            )

            average = result.scalar()

            connection.close()
            self._connection().dispose()

            return average

    def similarity_median(self, report_id: ReportId) -> float:
        pass
