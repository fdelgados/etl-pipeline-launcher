import unittest
from parameterized import parameterized
from hypothesis import given, strategies as st

from duplicates.shared.domain.model.similarity_threshold import (
    SimilarityThreshold,
)


class TestSimilarityThreshold(unittest.TestCase):
    @parameterized.expand(["a string", (10,), (0o10,), (0x10,)])
    def test_if_it_raises_an_exception_if_type_is_wrong(self, value) -> None:
        with self.assertRaises(ValueError):
            SimilarityThreshold(value)

    def test_if_it_raises_an_exception_if_value_is_lower_than_accepted(
        self,
    ) -> None:

        with self.assertRaises(ValueError):
            SimilarityThreshold(SimilarityThreshold.min() - 0.1)

    def test_if_it_raises_an_exception_if_value_is_higher_than_accepted(
        self,
    ) -> None:

        with self.assertRaises(ValueError):
            SimilarityThreshold(SimilarityThreshold.max() + 0.1)

    @given(
        st.floats(
            min_value=SimilarityThreshold.min(),
            max_value=SimilarityThreshold.max(),
        )
    )
    def test_if_it_not_raise_an_exception_if_value_is_valid(
        self,
        value: float,
    ) -> None:
        similarity_threshold = SimilarityThreshold(value)

        self.assertTrue(
            similarity_threshold == SimilarityThreshold(value),
            f"{similarity_threshold.value} should be equals to {value}",
        )
