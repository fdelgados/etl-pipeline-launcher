import abc

from typing import List

from .aggregate import AggregateRoot


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add(self, aggregate: AggregateRoot) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, aggregate: AggregateRoot) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def find(self, **kwargs) -> AggregateRoot:
        raise NotImplementedError

    @abc.abstractmethod
    def find_all(self, **kwargs) -> List[AggregateRoot]:
        raise NotImplementedError
