import unittest
from hypothesis import given
import hypothesis.strategies as st

from corpus.etl.domain.model.etl import EtlId


class EtlIdTest(unittest.TestCase):
    @given(st.uuids(version=3))
    def tests_if_it_raises_exception_when_uuid_is_invalid(self, uuid: str) -> None:
        with self.assertRaises(ValueError):
            EtlId(str(uuid))

    @given(st.uuids(version=4))
    def tests_if_it_not_raises_exception_when_uuid_is_valid(self, uuid: str) -> None:
        etl_id = EtlId(str(uuid))

        self.assertTrue(etl_id == EtlId(str(uuid)))


