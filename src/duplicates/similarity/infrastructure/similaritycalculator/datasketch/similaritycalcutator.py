import re
import pandas as pd
import xxhash

from typing import List, Set

from datasketch import MinHash, LeanMinHash

from duplicates.similarity.domain.model.duplicate import (
    Duplicate,
    DuplicateRepository,
)
from duplicates.similarity.domain.service.similaritycalculator import (
    SimilarityCalculator,
)
from duplicates.report.domain.model.report import Report
from duplicates.shared.domain.model.k_shingle_size import KShingleSize

import shared.infrastructure.environment.globalvars as glob
from shared.domain.model.valueobject.url import Url


class SimilarityCalculatorImpl(SimilarityCalculator):
    def __init__(self, duplicate_repository: DuplicateRepository):
        self._duplicate_repository = duplicate_repository

    def calculate(self, report: Report):
        content_file = glob.settings.duplicates_content_file(report.name)

        data_frame = pd.read_csv(content_file)
        minhashes = _compute_minhashes(data_frame, report.k_shingle_size)

        self._compute_similarities(report, minhashes, data_frame)

    def _compute_similarities(
        self, report: Report, minhashes, pages: pd.DataFrame
    ):
        num_of_minhashes = len(minhashes)

        for x in range(num_of_minhashes):
            page_x = pages.iloc[x]
            url_x = page_x["url"]

            for y in range(num_of_minhashes):
                if x >= y:
                    continue

                similarity = minhashes[x].jaccard(minhashes[y])

                if similarity < report.similarity_threshold.value:
                    continue

                page_y = pages.iloc[y]
                url_y = page_y["url"]

                duplicate = Duplicate(
                    report.report_id, Url(url_x), Url(url_y), similarity
                )

                self._duplicate_repository.add(duplicate)


def _tokenize(text: str) -> List:
    return re.split(r"\W+", text)


def _minhash(tokens: Set[str], num_of_permutations: int = 128) -> LeanMinHash:
    min_hash = MinHash(
        num_perm=num_of_permutations, hashfunc=xxhash.xxh64_intdigest
    )

    for token in tokens:
        min_hash.update(token.encode("utf8"))

    return LeanMinHash(min_hash)


def _shingle(words: List[str], size: KShingleSize) -> Set:
    shingles = set()

    for index in range(len(words) - size.value + 1):
        shingle = words[index : index + size.value]
        shingle = " ".join(shingle)

        shingles.add(shingle)

    return shingles


def _compute_minhashes(
    pages: pd.DataFrame, k_shingle_size: KShingleSize
) -> List[LeanMinHash]:
    minhashes = []

    for _, row in pages.iterrows():
        minhashes.append(
            _minhash(_shingle(_tokenize(row["content"]), k_shingle_size))
        )

    return minhashes
