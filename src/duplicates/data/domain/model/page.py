import abc

from shared.domain.model.value_object.url import Url


class Page:
    def __init__(self, url: Url, content: str, datalayer: dict):
        self._url = url
        self._content = content
        self._datalayer = datalayer

    @property
    def url(self) -> Url:
        return self._url

    @property
    def content(self) -> str:
        return self._content

    @property
    def datalayer(self) -> dict:
        return self._datalayer


class PageRetriever(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def retrieve_all(self, corpus: str):
        raise NotImplementedError
