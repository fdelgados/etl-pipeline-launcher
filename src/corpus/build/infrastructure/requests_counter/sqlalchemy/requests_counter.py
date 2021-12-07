from shared.infrastructure.persistence.sqlalchemy.dbal import DbalService

from corpus.build.domain.event.extraction_failed import ExtractionFailed
from corpus.build.domain.model.build import BuildId, Build
from corpus.build.domain.service.requests_counter import RequestsCounter
from corpus.build.domain.model.page import PageRepository


class RequestsCounterImpl(RequestsCounter):
    def __init__(
        self,
        db_service: DbalService,
        page_repository: PageRepository,
    ):
        self._db_service = db_service
        self._page_repository = page_repository

    def count_successful(self, build: Build) -> int:
        return self._page_repository.count_by_build(build.id)

    def count_failed(self, build_id: BuildId) -> int:
        sentence = """
                SELECT COUNT(*) AS requests FROM event_store
                WHERE JSON_UNQUOTE(
                    JSON_EXTRACT(event_data, "$.build_id")
                ) = :build_id
                AND event_name = :event
            """

        result = self._db_service.execute(
            sentence,
            build_id=build_id.value,
            event=ExtractionFailed.type_name(),
        )

        return result.scalar()
