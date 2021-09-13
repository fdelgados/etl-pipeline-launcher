from __future__ import annotations

from corpus.etl.domain.model.url import Url
from .. import EntityBuilder


class UrlCreator(EntityBuilder):
    def __init__(self):
        super().__init__()

        self._address = "https://www.google.com"

    def as_invalid(self) -> UrlCreator:
        self._address = "foo"

        return self

    def with_address(self, address: str) -> UrlCreator:
        self._address = address

        return self

    def build(self) -> Url:
        return Url(self._address)
