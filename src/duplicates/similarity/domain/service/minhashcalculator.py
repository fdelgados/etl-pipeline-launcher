import abc

from duplicates.shared.domain.model.k_shingle_size import KShingleSize
from duplicates.similarity.domain.model.minhash import MinHash
from duplicates.data.domain.model.transformedpagecontent import (
    TransformedPageContent,
)


class MinHashCalculator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def calculate(
        self,
        page_content: TransformedPageContent,
        k_shingle_size: KShingleSize,
    ) -> MinHash:
        raise NotImplementedError
