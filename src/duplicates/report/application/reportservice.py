from __future__ import annotations

from dataclasses import dataclass

from datetime import datetime

from shared.domain.bus.command import Command, CommandHandler
from shared.domain.bus.query import Query, QueryHandler, Response
from shared.domain.bus.event import EventBus
from shared.domain.errors.errors import Errors, ApplicationError
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
from duplicates.report.domain.service.statsretriever import (
    ReportStatsRetriever,
)


@dataclass(frozen=True)
class ReportCreatorCommand(Command):
    report_id: str
    corpus: str
    similarity_threshold: float
    k_shingle_size: int
    user: User
    similarity_threshold_margin: float = 0.0


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
            command.similarity_threshold_margin,
        )

        self._report_repository.save(report)

        self._event_bus.publish(*report.pull_events())


@dataclass(frozen=True)
class ReportProgressQuery(Query):
    report_id: str


class ReportProgressResponse(Response):
    def __init__(self, report_dto: ReportDto):
        self._report_dto = report_dto

    def value(self) -> ReportDto:
        return self._report_dto


class ReportProgressQueryHandler(QueryHandler):
    def __init__(
        self,
        report_repository: ReportRepository,
        stats_retriever: ReportStatsRetriever,
    ):
        self._report_repository = report_repository
        self._assembler = ReportAssembler(stats_retriever)

    def handle(self, query: ReportProgressQuery) -> ReportProgressResponse:
        report = self._report_repository.report_of_id(
            ReportId(query.report_id)
        )

        if not report:
            raise ApplicationError(
                Errors.entity_not_found(
                    entity_name="Report", entity_id=query.report_id
                )
            )

        return ReportProgressResponse(self._assembler.assemble(report))


@dataclass(frozen=True)
class ReportDto:
    id: str
    name: str
    corpus_name: str
    total_pages: int
    analyzed_pages: int
    duplicates_found: int
    started_by: str
    started_on: datetime
    completed_on: datetime
    status: dict
    similarity_threshold: float
    k_shingle_size: int
    duplication_ratio: float
    duplication_average: float
    duplication_median: float


class ReportAssembler:
    def __init__(self, stats_retriever: ReportStatsRetriever):
        self._stats_retriever = stats_retriever

    def assemble(self, report: Report):
        report_stats = self._stats_retriever.retrieve(report)

        return ReportDto(
            report.report_id.value,
            report.name,
            report.from_corpus,
            report.total_pages,
            report_stats.analyzed_pages,
            report_stats.duplicated_pages,
            report.created_by,
            report.started_on,
            report.completed_on,
            report.status.serialize(),
            report.similarity_threshold.value,
            report.k_shingle_size.value,
            0.0,
            0.0,
            0.0,
        )


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
