from duplicates.report.domain.model.report import Report
from duplicates.similarity.domain.service.minhashcalculator import (
    MinHashCalculator,
)

from duplicates.data.domain.model.transformedpagecontent import (
    TransformedPageContentRepository,
)


class MinHashGenerator:
    def __init__(
        self,
        content_repository: TransformedPageContentRepository,
        minhash_calculator: MinHashCalculator,
    ):
        self._content_repository = content_repository
        self._minhash_calculator = minhash_calculator

    def generate(self, report: Report):
        pages = self._content_repository.get_all(report.tenant_id)
        minhashes = {}
        for page in pages:
            minhashes[page.url.address] = self._minhash_calculator.calculate(
                page,
                report.k_shingle_size,
            )

        return minhashes
