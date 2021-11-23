from typing import List

from duplicates.shared.domain.model.k_shingle_size import KShingleSize
from duplicates.similarity.domain.service.minhashcalculator import (
    MinHashCalculator,
)

from duplicates.data.domain.model.transformedpagecontent import (
    TransformedPageContent,
)


class MinHashGenerator:
    def __init__(self, minhash_calculator: MinHashCalculator):
        self._minhash_calculator = minhash_calculator

    def generate(
        self, k_shingle_size: KShingleSize, pages: List[TransformedPageContent]
    ):
        minhashes = {}
        for page in pages:
            minhashes[page.url.address] = self._minhash_calculator.calculate(
                page,
                k_shingle_size,
            )

        return minhashes
