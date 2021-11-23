from dataclasses import dataclass

from shared.domain.bus.command import Command, CommandHandler
from shared.domain.bus.query import Query, QueryHandler, Response
from shared.domain.bus.event import EventBus
from shared.domain.service.logging.logger import Logger
from shared.domain.model.entity.user import User
from duplicates.shared.domain.model.similarity_threshold import (
    SimilarityThreshold,
)
from duplicates.shared.domain.model.k_shingle_size import KShingleSize
from duplicates.report.domain.model.report import (
    Report,
    ReportRepository,
    ReportId,
)


@dataclass(frozen=True)
class ReportCreatorCommand(Command):
    report_id: str
    corpus: str
    similarity_threshold: float
    k_shingle_size: int
    user: User


class ReportCreatorCommandHandler(CommandHandler):
    def __init__(
        self,
        logger: Logger,
        report_repository: ReportRepository,
        event_bus: EventBus,
    ):
        self._logger = logger
        self._report_repository = report_repository
        self._event_bus = event_bus

    def handle(self, command: ReportCreatorCommand) -> None:
        self._logger.info("Create a new pages near duplicates report")

        report = Report(
            ReportId(command.report_id),
            self._report_repository.generate_unique_name(),
            command.corpus,
            command.user,
            KShingleSize(command.k_shingle_size),
            SimilarityThreshold(command.similarity_threshold),
        )

        self._report_repository.save(report)

        self._event_bus.publish(*report.pull_events())


@dataclass(frozen=True)
class NextIdentityQuery(Query):
    pass


class NextIdentityResponse(Response):
    def __init__(self, report_id: ReportId):
        self._report_id = report_id

    def value(self) -> str:
        return self._report_id.value


class NextIdentityQueryHandler(QueryHandler):
    def __init__(self, report_repository: ReportRepository):
        self._report_repository = report_repository

    def handle(self, query: NextIdentityQuery) -> NextIdentityResponse:
        return NextIdentityResponse(self._report_repository.next_identity())
