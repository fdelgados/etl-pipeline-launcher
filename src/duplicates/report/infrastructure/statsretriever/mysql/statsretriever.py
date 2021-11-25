from shared.infrastructure.persistence.sqlalchemy.dbal import DbalService

from duplicates.similarity.domain.event.pageanalyzed import PageAnalyzed
from duplicates.similarity.domain.event.duplicitydetected import (
    DuplicityDetected,
)
from duplicates.report.domain.model.report import Report
from duplicates.report.domain.service.statsretriever import (
    ReportStatsRetriever,
    ReportStats,
)


class ReportStatsRetrieverImpl(ReportStatsRetriever):
    def __init__(self, db_service: DbalService):
        self._db_service = db_service

    def retrieve(self, report: Report) -> ReportStats:
        return ReportStats(
            self._get_stats_from_event_store(report, PageAnalyzed.type_name()),
            self._get_stats_from_event_store(
                report, DuplicityDetected.type_name()
            ),
        )

    def _get_stats_from_event_store(
        self, report: Report, event_type: str
    ) -> int:

        sentence = """
            SELECT COUNT(*) AS requests FROM event_store
            WHERE report_id = :report_id
            AND event_name = :event
        """

        result = self._db_service.execute(
            sentence,
            report_id=report.report_id.value,
            event=event_type,
        )

        return result.scalar()
