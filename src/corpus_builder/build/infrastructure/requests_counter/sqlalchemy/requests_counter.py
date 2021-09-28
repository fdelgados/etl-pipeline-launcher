from shared.infrastructure.persistence.sqlalchemy.dbal import DbalService

from corpus_builder.build.domain.event.page_added import PageAdded
from corpus_builder.build.domain.event.extraction_failed import ExtractionFailed
from corpus_builder.build.domain.model.build import BuildId
from corpus_builder.build.domain.service.requests_counter import RequestsCounter


class RequestsCounterImpl(RequestsCounter):
    def __init__(self, db_service: DbalService):
        self._db_service = db_service

    def count_successful(self, build_id: BuildId) -> int:
        return self._count_by_result(build_id, PageAdded.type_name())

    def count_failed(self, build_id: BuildId) -> int:
        return self._count_by_result(build_id, ExtractionFailed.type_name())

    def _count_by_result(self, build_id: BuildId, domain_event_type: str) -> int:
        sentence = """
            SELECT COUNT(*) AS requests FROM event_store
            WHERE build_id = :build_id
            AND event_name = :event
        """

        result = self._db_service.execute(
            sentence,
            build_id=build_id.value,
            event=domain_event_type,
        )

        return result.scalar()
