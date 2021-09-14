import unittest
from parameterized import parameterized
from hypothesis import given, strategies as st

from duplicates.shared.domain.model.k_shingle_size import KShingleSize


class KShingleSizeTest(unittest.TestCase):
    @parameterized.expand(["a string", (1.0,)])
    def test_if_it_raises_an_exception_when_type_is_wrong(self, value) -> None:
        with self.assertRaises(ValueError):
            KShingleSize(value)

    def test_if_it_raises_an_exception_when_value_is_lower_than_accepted(self) -> None:
        with self.assertRaises(ValueError):
            KShingleSize(KShingleSize.min() - 1)

    def test_if_it_raises_an_exception_when_value_is_higher_than_accepted(self) -> None:
        with self.assertRaises(ValueError):
            KShingleSize(KShingleSize.max() + 1)

    @given(
        st.integers(
            min_value=KShingleSize.min(), max_value=KShingleSize.max()
        )
    )
    def test_if_it_not_raise_an_exception_when_value_is_valid(
        self, value: int
    ) -> None:
        k_shingle_size = KShingleSize(value)

        self.assertTrue(
            k_shingle_size == KShingleSize(value),
            f"{k_shingle_size.value} should be equals to {value}",
        )
