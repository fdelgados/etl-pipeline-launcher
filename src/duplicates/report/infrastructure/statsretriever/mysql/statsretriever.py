from shared.infrastructure.persistence.sqlalchemy.dbal import DbalService

from duplicates.similarity.domain.event.pageanalyzed import PageAnalyzed

from duplicates.report.domain.model.report import (
    Report,
    ReportId,
    DuplicateRepository,
)
from duplicates.report.domain.service.statsretriever import (
    ReportStatsRetriever,
    ReportStats,
)


class ReportStatsRetrieverImpl(ReportStatsRetriever):
    def __init__(
        self,
        db_service: DbalService,
        duplicate_repository: DuplicateRepository,
    ):
        self._db_service = db_service
        self._duplicate_repository = duplicate_repository

    def retrieve(self, report: Report) -> ReportStats:
        analyzed_pages = self._analyzed_pages(report.report_id)
        duplicates = self._number_of_duplicates(report.report_id)

        return ReportStats(
            analyzed_pages,
            duplicates,
            float(self._similarity_average(report.report_id)),
            0.0,  # TODO calculate median
            float(duplicates / analyzed_pages) if analyzed_pages > 0 else 0.0,
        )

    def _analyzed_pages(self, report_id: ReportId) -> int:

        sentence = """
            SELECT COUNT(DISTINCT aggregate_id) AS requests FROM event_store
            WHERE JSON_UNQUOTE(
                JSON_EXTRACT(event_data, "$.report_id")
            ) = :report_id
            AND event_name = :event
        """

        result = self._db_service.execute(
            sentence,
            report_id=report_id.value,
            event=PageAnalyzed.type_name(),
        )

        return result.scalar()

    def _number_of_duplicates(self, report_id: ReportId) -> int:
        return self._duplicate_repository.count(report_id)

    def _similarity_average(self, report_id: ReportId) -> float:
        average = self._duplicate_repository.similarity_average(report_id)

        if average is not None:
            return average

        return 0.0
