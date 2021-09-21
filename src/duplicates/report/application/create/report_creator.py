from dataclasses import dataclass

from shared_context import Command, CommandHandler
from shared.infrastructure.event import DomainEventDispatcher
from shared.domain.service.logging.logger import Logger
from shared.domain.model.user.user import User
from duplicates.shared.domain.model.similarity_threshold import SimilarityThreshold
from duplicates.shared.domain.model.k_shingle_size import KShingleSize
from duplicates.report.domain.model.report import Report, ReportRepository


@dataclass(frozen=True)
class ReportCreatorCommand(Command):
    similarity_threshold: float
    k_shingle_size: int
    user: User


class ReportCreator(CommandHandler):
    def __init__(self, logger: Logger, report_repository: ReportRepository):
        self._logger = logger
        self._report_repository = report_repository

    def handle(self, command: ReportCreatorCommand):
        self._logger.info("Create a new pages near duplicates report")

        report = Report(
            self._report_repository.next_identity(),
            self._report_repository.generate_unique_name(),
            command.user,
            KShingleSize(command.k_shingle_size),
            SimilarityThreshold(command.similarity_threshold),
        )

        self._report_repository.save(report)

        DomainEventDispatcher.dispatch(report.events())

        return report.id
