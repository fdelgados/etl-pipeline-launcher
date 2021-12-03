import unittest

from unit.builders.pagecreator import PageCreator


class TestPage(unittest.TestCase):
    def test_if_redirected_url_is_not_fully_indexable(self) -> None:
        page = PageCreator().with_redirection().build()

        self.assertTrue(page.is_redirection())
        self.assertFalse(page.is_fully_indexable())

    def test_if_page_with_canonical_url_is_not_fully_indexable(self) -> None:
        page = PageCreator().with_canonical_url().build()

        self.assertFalse(page.is_canonical, "Page should be non canonical")
        self.assertFalse(
            page.is_fully_indexable(), "Page should be non indexable"
        )
