import abc

from corpus.etl.domain.model.etl import Etl
from corpus.etl.domain.model.page import Page
from corpus.etl.domain.model.url import Url


__all__ = ['PageRetriever', 'RetrievalError', 'PageRetrieverFatalError']


class PageRetrieverFatalError(RuntimeError):
    pass


class RetrievalError(RuntimeError):
    pass


class PageRetriever(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def retrieve(self, url: Url, etl: Etl) -> Page:
        raise NotImplementedError
