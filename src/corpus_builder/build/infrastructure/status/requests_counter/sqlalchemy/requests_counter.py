from shared.infrastructure.persistence.sqlalchemy.dbal import DbalService

from corpus_builder.build.domain.event.page_added import PageAdded
from corpus_builder.build.domain.event.extraction_failed import ExtractionFailed
from corpus_builder.build.domain.model.build import BuildId
from corpus_builder.build.domain.service.status.requests_counter import RequestsCounter


class RequestsCounterImpl(RequestsCounter):
    def __init__(self, db_service: DbalService):
        self._db_service = db_service

    def count(self, build_id: BuildId):
        sentence = """
            SELECT COUNT(*) AS requests FROM event_store
            WHERE build_id = :build_id
            AND event_name IN :requests_events
        """

        result = self._db_service.execute(
            sentence,
            build_id=build_id.value,
            requests_events=[ExtractionFailed.type_name(), PageAdded.type_name()],
        )

        return result.scalar()
