from typing import List, Optional

import shared.infrastructure.environment.globalvars as global_vars

from shared.domain.model.valueobject.url import Url
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

    def search_all_by_report_id(
        self,
        report_id: ReportId,
        limit: Optional[int] = None,
        offset: Optional[int] = 0,
    ) -> List[Duplicate]:

        duplicates = []

        sentence = """
            SELECT url, duplicate_url, similarity
            FROM report_duplicates
            WHERE report_id = UUID_TO_BIN(:report_id)
            ORDER BY similarity
        """

        if limit is not None:
            sentence += f" LIMIT {limit} OFFSET {offset}"

        with self._connection().connect() as connection:
            result = connection.execute(
                self._statement(sentence), report_id=report_id.value
            )

            rows = result.all()

            for row in rows:
                duplicates.append(
                    Duplicate(
                        report_id,
                        Url(row["url"]),
                        Url(row["duplicate_url"]),
                        float(row["similarity"]),
                    )
                )

            connection.close()
            self._connection().dispose()

            return duplicates

    def count(self, report_id: ReportId) -> int:
        sentence = """
            SELECT COUNT(DISTINCT url) AS num_duplicates FROM report_duplicates
            WHERE report_id = UUID_TO_BIN(:report_id)
        """

        with self._connection().connect() as connection:
            result = connection.execute(
                self._statement(sentence), report_id=report_id.value
            )

            duplicates = result.scalar()

            connection.close()
            self._connection().dispose()

            return duplicates

    def similarity_average(self, report_id: ReportId) -> float:
        sentence = """
            SELECT AVG(similarity) AS similarity_average FROM report_duplicates
            WHERE report_id = UUID_TO_BIN(:report_id)
        """

        with self._connection().connect() as connection:
            result = connection.execute(
                self._statement(sentence), report_id=report_id.value
            )

            average = result.scalar()

            connection.close()
            self._connection().dispose()

            return average

    def similarity_median(self, report_id: ReportId) -> float:
        pass
