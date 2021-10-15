from shared.domain.bus.event import DomainEventSubscriber
from duplicates.data.domain.event.dataloaded import DataLoaded
from duplicates.report.domain.model.report import ReportRepository, ReportId
from duplicates.similarity.domain.service.similaritycalculator import (
    SimilarityCalculator,
)


class CalculateSimilaritiesOnDataLoaded(DomainEventSubscriber):
    def __init__(
        self,
        report_repository: ReportRepository,
        similarity_calculator: SimilarityCalculator,
    ):
        super().__init__()

        self._report_repository = report_repository
        self._similarity_calculator = similarity_calculator

    def handle(self, domain_event: DataLoaded) -> None:
        report = self._report_repository.report_of_id(ReportId(domain_event.report_id))

        if not report:
            raise Exception

        self._similarity_calculator.calculate(report)
