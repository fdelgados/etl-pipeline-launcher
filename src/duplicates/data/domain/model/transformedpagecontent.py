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
    def save_all(self, report_name: str, transformed_page_content: List[TransformedPageContent]):
        raise NotImplementedError
