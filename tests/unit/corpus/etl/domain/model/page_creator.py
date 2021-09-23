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
        self._status = HTTPStatus.OK.phrase
        self._status_code = HTTPStatus.OK
        self._canonical_url = None
        self._final_url = None
        self._corpus_name = None
        self._tenant_id = None

    def with_redirection(self, final_url: Optional[Url] = None) -> PageCreator:
        self._status = HTTPStatus.MOVED_PERMANENTLY.phrase
        self._status_code = HTTPStatus.MOVED_PERMANENTLY

        if not final_url:
            final_url = self.fake.url()

        self._final_url = final_url

        return self

    def with_canonical_url(self, url: Optional[Url] = None) -> PageCreator:
        if not url:
            url = Url(self.fake.url())

        self._canonical_url = url

        return self

    def with_corpus_name(self, corpus_name: str) -> PageCreator:
        self._corpus_name = corpus_name

        return self

    @property
    def corpus_name(self) -> str:
        return (
            self._corpus_name if self._corpus_name else self.fake.text(max_nb_chars=25)
        )

    def with_tenant_id(self, tenant_id: str) -> PageCreator:
        self._tenant_id = tenant_id

        return self

    @property
    def tenant_id(self) -> str:
        return self._tenant_id if self._tenant_id else self.fake.uuid4()

    def build(self) -> Page:
        page = Page(
            Url(self._fake.url()),
            BuildId(),
            self.tenant_id,
            self._status_code,
            self._status,
            self.fake.date_time_this_month(),
            self.corpus_name,
        )

        if self._canonical_url:
            page.canonical_url = self._canonical_url

        if self._final_url:
            page.final_url = self._final_url

        return page
