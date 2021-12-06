from __future__ import annotations

import abc

from typing import Optional

from datetime import datetime
from dataclasses import dataclass, field
from http import HTTPStatus

from shared.domain.model.valueobject.url import Url


class PageRequesterFatalError(RuntimeError):
    pass


class RetrievalError(RuntimeError):
    pass


@dataclass
class Response:
    status_code: int
    status: str
    modified_on: datetime
    request: Request
    h1: str = ""
    title: str = ""
    content: dict = field(init=False, default_factory=dict)
    final_url: Optional[Url] = field(default=None)
    canonical_url: Optional[Url] = field(default=None)
    is_indexable: bool = False
    datalayer: dict = field(init=False, default_factory=dict)

    @property
    def url(self) -> Url:
        return self.request.url

    @property
    def request_headers(self) -> dict:
        return self.request.headers

    @property
    def is_successful(self) -> bool:
        if self.status_code == HTTPStatus.OK:
            return True

        return self.status_code == HTTPStatus.NOT_MODIFIED


@dataclass
class Request:
    url: Url
    headers: dict = field(init=False, default_factory=dict)
    excluded_tags: list = field(init=False, default_factory=list)
    excluded_selectors: list = field(init=False, default_factory=list)
    selector_mapping: dict = field(init=False, default_factory=dict)


class PageRequester(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def request(self, request: Request) -> Response:
        raise NotImplementedError
