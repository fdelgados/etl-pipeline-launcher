import unittest
from hypothesis import given
import hypothesis.strategies as st

from corpus.build.domain.model.build import BuildId


class TestBuildId(unittest.TestCase):
    @given(st.uuids(version=3))
    def test_if_it_raises_exception_when_uuid_is_invalid(self, uuid: str) \
            -> None:

        with self.assertRaises(ValueError):
            BuildId(str(uuid))

    @given(st.uuids(version=4))
    def test_if_it_not_raises_exception_when_uuid_is_valid(self, uuid: str) \
            -> None:

        build_id = BuildId(str(uuid))

        self.assertTrue(build_id == BuildId(str(uuid)))
