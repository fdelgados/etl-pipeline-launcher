import abc
from typing import Dict, Optional
from datetime import datetime
from http import HTTPStatus

from shared.domain.model.value_object.url import Url
from shared.domain.model.aggregate import AggregateRoot
from shared.domain.model.repository import Repository

from corpus_builder.build.domain.event.page_added import PageAdded
from corpus_builder.build.domain.model.build import BuildId


class Page(AggregateRoot):
    def __init__(
        self,
        url: Url,
        build_id: BuildId,
        tenant_id: str,
        status_code: int,
        status: str,
        modified_on: datetime,
        corpus_name: str,
    ):
        self._url = url
        self._build_id = build_id
        self._tenant_id = tenant_id
        self._status_code = status_code
        self._status = status
        self._modified_on = modified_on
        self._corpus_name = corpus_name
        self._h1 = None
        self._title = None
        self._is_indexable = None
        self._final_url = None
        self._canonical_url = None
        self._datalayer = {}
        self._content = {}

        page_requested = PageAdded(
            self._tenant_id,
            self._build_id.value,
            self._url.address,
            self._status_code,
            self._status,
            self._modified_on,
            self._corpus_name,
        )

        self.record_event(page_requested)

    def content_by_tag(self, tag_name: str) -> Optional[str]:
        return self._content.get(tag_name)

    @property
    def url(self) -> Url:
        return self._url

    @property
    def corpus_name(self) -> str:
        return self._corpus_name

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def status(self) -> str:
        return self._status

    @property
    def final_url(self) -> Optional[Url]:
        return self._final_url

    @final_url.setter
    def final_url(self, final_url: Url) -> None:
        self._final_url = final_url

    @property
    def h1(self) -> str:
        return self._h1

    @h1.setter
    def h1(self, h1: str) -> None:
        self._h1 = h1

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        self._title = title

    @property
    def is_indexable(self) -> bool:
        return self._is_indexable

    def mark_as_indexable(self) -> None:
        self._is_indexable = True

    def is_fully_indexable(self) -> bool:
        if not self.is_ok():
            return False

        if not self._is_indexable:
            return False

        return self.is_canonical

    def is_redirection(self) -> bool:
        return self._status_code in [HTTPStatus.MOVED_PERMANENTLY, HTTPStatus.FOUND]

    def is_ok(self) -> bool:
        return self._status_code in [HTTPStatus.OK, HTTPStatus.NOT_MODIFIED]

    def is_unmodified(self) -> bool:
        return self._status_code == HTTPStatus.NOT_MODIFIED

    @property
    def is_canonical(self) -> bool:
        if not self._canonical_url:
            return True

        return self.is_self_canonical

    @property
    def is_self_canonical(self) -> bool:
        if not self._canonical_url:
            return False

        return self._canonical_url == self.url

    @property
    def canonical_url(self) -> Optional[Url]:
        return self._canonical_url

    @canonical_url.setter
    def canonical_url(self, canonical_url: Optional[Url] = None) -> None:
        self._canonical_url = canonical_url

    @property
    def datalayer(self) -> Dict:
        return self._datalayer

    @datalayer.setter
    def datalayer(self, datalayer: Dict) -> None:
        self._datalayer = datalayer

    @property
    def content(self) -> Optional[Dict]:
        return self._content

    @content.setter
    def content(self, content: Dict) -> None:
        self._content = content

    def content_text(self) -> str:
        return " ".join([text_piece for _, text_piece in self._content.items()])

    @property
    def modified_on(self) -> datetime:
        return self._modified_on

    def __repr__(self):
        return "<Page {} ({})>".format(self._url.address, self._status_code)

    def __str__(self):
        return self._url.address


class UnableToSavePageError(RuntimeError):
    pass


class PageRepository(Repository, metaclass=abc.ABCMeta):
    pass
