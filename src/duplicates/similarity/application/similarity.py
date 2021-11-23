from __future__ import annotations

from typing import List, Dict

from shared.domain.bus.event import DomainEventSubscriber, EventBus
from shared.domain.errors.errors import Errors, ApplicationError

from duplicates.data.domain.event.dataloaded import DataLoaded
from duplicates.data.domain.model.transformedpagecontent import (
    TransformedPageContentRepository,
    TransformedPageContent,
)
from duplicates.report.domain.model.report import (
    ReportRepository,
    Report,
    ReportId,
)
from duplicates.similarity.domain.event.pageanalyzed import PageAnalyzed
from duplicates.similarity.domain.model.duplicate import (
    Duplicate,
    DuplicateRepository,
)
from duplicates.similarity.domain.service.minhashgenerator import (
    MinHashGenerator,
)

from duplicates.similarity.domain.model.minhash import (
    MinHashRepository,
    MinHash,
)


class CalculateSimilaritiesOnDataLoaded(DomainEventSubscriber):
    def __init__(self, similarity_calculator: SimilarityCalculatorService):
        super().__init__()

        self._similarity_calculator = similarity_calculator

    def handle(self, domain_event: DataLoaded) -> None:
        self._similarity_calculator.calculate(ReportId(domain_event.report_id))


class SimilarityCalculatorService:
    def __init__(
        self,
        report_repository: ReportRepository,
        minhash_generator: MinHashGenerator,
        minhash_repository: MinHashRepository,
        page_repository: TransformedPageContentRepository,
        duplicate_repository: DuplicateRepository,
        event_bus: EventBus,
    ):
        self._report_repository = report_repository
        self._minhash_generator = minhash_generator
        self._minhash_repository = minhash_repository
        self._page_repository = page_repository
        self._duplicate_repository = duplicate_repository
        self._event_bus = event_bus

    def calculate(self, report_id: ReportId) -> None:
        report = self._report_repository.report_of_id(report_id)

        if not report:
            raise ApplicationError(
                Errors.entity_not_found(
                    entity_name="Report", entity_id=report_id.value
                )
            )

        pages = self._page_repository.get_all(report.tenant_id)

        minhashes = self._minhash_generator.generate(
            report.k_shingle_size, pages
        )

        self._minhash_repository.add_all_of_tenant(report.tenant_id, minhashes)

        self._duplicate_pair(report, minhashes, pages)

    def _duplicate_pair(
        self,
        report: Report,
        minhashes: Dict[str, MinHash],
        pages: List[TransformedPageContent],
    ):
        num_of_pages = len(pages)

        for x in range(num_of_pages):
            page_x = pages[x]
            url_x = page_x.url
            minhash_x = minhashes[url_x.address]

            for y in range(num_of_pages):
                if x >= y:
                    continue

                page_y = pages[y]
                url_y = page_y.url
                address_y = url_y.address

                similarity = minhash_x.jaccard(minhashes[address_y])

                if similarity < report.similarity_threshold.value:
                    continue

                duplicate = Duplicate(
                    report.report_id, url_x, url_y, similarity
                )

                self._duplicate_repository.add(duplicate)

                self._event_bus.publish(*duplicate.pull_events())

            self._event_bus.publish(
                PageAnalyzed(report.report_id.value, url_x.address)
            )
