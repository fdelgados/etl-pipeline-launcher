import re
import xxhash

from typing import List, Set

from datasketch import MinHash, LeanMinHash

from duplicates.shared.domain.model.k_shingle_size import KShingleSize
from duplicates.similarity.domain.model.minhash import MinHash as MinHashVO
from duplicates.similarity.domain.service.minhashcalculator import (
    MinHashCalculator,
)
from duplicates.data.domain.model.transformedpagecontent import (
    TransformedPageContent,
)


class MinHashCalculatorImpl(MinHashCalculator):
    _NUM_OF_PERMUTATIONS = 128

    def calculate(
        self,
        page_content: TransformedPageContent,
        k_shingle_size: KShingleSize,
    ) -> MinHashVO:
        tokens = re.split(r"\W+", page_content.content)
        shingles = _shingle(tokens, k_shingle_size)

        minhash = MinHash(
            num_perm=self._NUM_OF_PERMUTATIONS,
            hashfunc=xxhash.xxh64_intdigest,
        )

        for shingle in shingles:
            minhash.update(shingle.encode("utf8"))

        return MinHashVO(LeanMinHash(minhash))


def _shingle(words: List[str], size: KShingleSize) -> Set:
    shingles = set()

    for index in range(len(words) - size.value + 1):
        shingle = words[index : index + size.value]
        shingle = " ".join(shingle)

        shingles.add(shingle)

    return shingles
