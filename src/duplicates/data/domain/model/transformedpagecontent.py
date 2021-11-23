import abc

from typing import List

from shared.domain.model.valueobject.url import Url


class TransformedPageContent:
    def __init__(self, url: Url, content: str):
        self._url = url
        self._content = content

    @property
    def url(self) -> Url:
        return self._url

    @property
    def content(self) -> str:
        return self._content


class TransformedPageContentRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_all(
        self,
        tenant_id: str,
        transformed_page_content: List[TransformedPageContent],
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self, tenant_id: str) -> List[TransformedPageContent]:
        raise NotImplementedError

    @abc.abstractmethod
    def size(self, tenant_id: str) -> int:
        raise NotImplementedError
