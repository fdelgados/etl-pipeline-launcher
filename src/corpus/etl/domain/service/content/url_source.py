import abc

from typing import Optional, List
from corpus.etl.domain.model.url import Url


__all__ = ['UrlSource', 'UrlSourceError']


class UrlSourceError(RuntimeError):
    pass


class UrlSource(metaclass=abc.ABCMeta):
    def retrieve(self, max_urls: Optional[int] = 0, **kwargs) -> List[Url]:
        raise NotImplementedError
