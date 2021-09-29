import abc

from corpus_builder.build.domain.model.page import Page
from shared.domain.model.value_object.url import Url
from corpus_builder.build.domain.model.build import Build
from corpus_builder.build.domain.model.corpus import Corpus


__all__ = ["PageRetriever", "RetrievalError", "PageRetrieverFatalError"]


class PageRetrieverFatalError(RuntimeError):
    pass


class RetrievalError(RuntimeError):
    pass


class PageRetriever(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def retrieve(self, url: Url, build: Build, corpus: Corpus) -> Page:
        raise NotImplementedError
