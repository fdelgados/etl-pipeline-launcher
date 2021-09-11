import unittest

from corpus.etl.domain.event.page_requested import PageRequested

from .page_creator import PageCreator


class PageTest(unittest.TestCase):
    def test_if_domain_event_has_been_recorded(self) -> None:
        page = PageCreator().build()

        events = page.events()

        self.assertEqual(len(events), 1, 'Page should have an event')
        self.assertIsInstance(events[0], PageRequested, 'Event should be PageRequested')

    def test_if_redirected_url_is_not_fully_indexable(self) -> None:
        page = PageCreator().with_redirection().build()

        self.assertTrue(page.is_redirection())
        self.assertFalse(page.is_fully_indexable())

    def test_if_page_with_canonical_url_is_not_fully_indexable(self) -> None:
        page = PageCreator().with_canonical_url().build()

        self.assertFalse(page.is_canonical, 'Page should be non canonical')
        self.assertFalse(page.is_fully_indexable(), 'Page should be non indexable')


if __name__ == "__main__":
    unittest.main()
