from shared.domain.bus.event import DomainEventSubscriber
from shared.domain.errors.errors import Errors, ApplicationError

from duplicates.data.domain.event.dataloaded import DataLoaded
from duplicates.report.domain.model.report import ReportRepository, ReportId
from duplicates.similarity.domain.service.similaritycalculator import (
    SimilarityCalculator,
)

from duplicates.similarity.domain.service.minhashgenerator import (
    MinHashGenerator,
)

from duplicates.similarity.domain.model.minhash import MinHashRepository


class CalculateSimilaritiesOnDataLoaded(DomainEventSubscriber):
    def __init__(
        self,
        report_repository: ReportRepository,
        similarity_calculator: SimilarityCalculator,
        minhash_generator: MinHashGenerator,
        minhash_repository: MinHashRepository,
    ):
        super().__init__()

        self._report_repository = report_repository
        self._similarity_calculator = similarity_calculator
        self._minhash_generator = minhash_generator
        self._minhash_repository = minhash_repository

    def handle(self, domain_event: DataLoaded) -> None:
        report = self._report_repository.report_of_id(
            ReportId(domain_event.report_id)
        )

        if not report:
            raise ApplicationError(
                Errors.entity_not_found(
                    entity_name="Report", entity_id=domain_event.report_id
                )
            )

        minhashes = self._minhash_generator.generate(report)

        self._minhash_repository.add_all_of_tenant(report.tenant_id, minhashes)

        self._similarity_calculator.calculate(report)
