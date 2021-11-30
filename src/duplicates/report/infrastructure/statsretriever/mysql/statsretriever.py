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
            self._get_analysis_stats(report),
            self._get_duplicity_stats(report),
        )

    def _get_analysis_stats(self, report: Report) -> int:

        sentence = """
            SELECT COUNT(*) AS requests FROM event_store
            WHERE report_id = :report_id
            AND event_name = :event
        """

        result = self._db_service.execute(
            sentence,
            report_id=report.report_id.value,
            event=PageAnalyzed.type_name(),
        )

        return result.scalar()

    def _get_duplicity_stats(self, report: Report) -> int:

        sentence = """
            SELECT COUNT(*) AS requests FROM event_store
            WHERE report_id = :report_id
            AND event_name = :event
            GROUP BY aggregate_id
        """

        result = self._db_service.execute(
            sentence,
            report_id=report.report_id.value,
            event=DuplicityDetected.type_name(),
        )

        return result.scalar()
