from __future__ import annotations

from http import HTTPStatus

from typing import Optional

from corpus_builder.build.domain.model.page import Page
from corpus_builder.build.domain.model.url import Url
from corpus_builder.build.domain.model.build import BuildId
from .. import EntityBuilder


class PageCreator(EntityBuilder):
    def __init__(self):
        super().__init__()
        self._status = HTTPStatus.OK
        self._status_code = HTTPStatus.OK.phrase
        self._canonical_url = None
        self._final_url = None

    def with_redirection(self, final_url: Optional[Url] = None) -> PageCreator:
        self._status = HTTPStatus.MOVED_PERMANENTLY
        self._status_code = HTTPStatus.MOVED_PERMANENTLY.phrase

        if not final_url:
            final_url = self.fake.url()

        self._final_url = final_url

        return self

    def with_canonical_url(self, url: Optional[Url] = None) -> PageCreator:
        if not url:
            url = Url(self.fake.url())

        self._canonical_url = url

        return self

    def build(self) -> Page:
        page = Page(
            Url(self._fake.url()),
            BuildId(),
            self._status,
            self._status_code,
            self.fake.date_time_this_month(),
        )

        if self._canonical_url:
            page.canonical_url = self._canonical_url

        if self._final_url:
            page.final_url = self._final_url

        return page
