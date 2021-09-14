from dataclasses import dataclass

from shared.infrastructure.event import DomainEventPublisher
from shared.infrastructure.security import authorization_required
from shared.domain.service.logging.logger import Logger
from shared.domain.model.user.user import User
from duplicates.shared.domain.model.similarity_threshold import SimilarityThreshold
from duplicates.shared.domain.model.k_shingle_size import KShingleSize
from duplicates.report.domain.model.report import (
    Report,
    ReportRepository
)


@dataclass(frozen=True)
class ReportCreatorCommand:
    similarity_threshold: float
    k_shingle_size: int


class ReportCreator:
    def __init__(self, logger: Logger, report_repository: ReportRepository):
        self._logger = logger
        self._report_repository = report_repository

    @authorization_required("create:near-duplicates-report")
    def create(self, user: User, command: ReportCreatorCommand):
        self._logger.info("Create a new pages near duplicates report")

        report = Report(
            self._report_repository.next_identity(),
            self._report_repository.generate_unique_name(),
            user,
            KShingleSize(command.k_shingle_size),
            SimilarityThreshold(command.similarity_threshold)
        )

        self._report_repository.save(report)

        DomainEventPublisher.publish(report.events())

        return report.id
