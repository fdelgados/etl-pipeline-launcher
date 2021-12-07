from typing import List, Dict

from duplicates.report.domain.model.report import (
    Duplicate,
    DuplicateRepository,
    Report,
)
from duplicates.similarity.domain.model.minhash import (
    MinHash,
    MinHashRepository,
)
from duplicates.data.domain.model.transformedpagecontent import (
    TransformedPageContentRepository,
    TransformedPageContent,
)
from duplicates.similarity.domain.service.similaritycalculator import (
    SimilarityCalculator,
)


class SimilarityCalculatorImpl(SimilarityCalculator):
    def __init__(
        self,
        duplicate_repository: DuplicateRepository,
        minhash_repository: MinHashRepository,
        page_repository: TransformedPageContentRepository,
    ):
        self._duplicate_repository = duplicate_repository
        self._minhash_repository = minhash_repository
        self._page_repository = page_repository

    def calculate(self, report: Report):
        pages = self._page_repository.get_all(report.tenant_id)

        minhashes = self._minhash_repository.get_all_of_tenant(
            report.tenant_id
        )

        self._calculate_similarities(report, minhashes, pages)

    def _calculate_similarities(
        self,
        report: Report,
        minhashes: Dict[str, MinHash],
        pages: List[TransformedPageContent],
    ):
        num_of_pages = len(pages)

        for x in range(num_of_pages):
            page_x = pages[x]
            url_x = page_x.url
            address_x = url_x.address

            for y in range(num_of_pages):
                if x >= y:
                    continue

                page_y = pages[y]
                url_y = page_y.url
                address_y = url_y.address

                similarity = minhashes[address_x].jaccard(minhashes[address_y])

                if similarity < report.similarity_threshold.value:
                    continue

                duplicate = Duplicate(
                    report.report_id, url_x, url_y, similarity
                )

                self._duplicate_repository.add(duplicate)
