import abc

from datetime import datetime

from typing import List

from shared.domain.model.valueobject.url import Url
from shared.domain.model.aggregate import AggregateRoot
from shared.domain.model.repository import Repository
from duplicates.check.domain.model.duplicitycheck import DuplicityCheckId


class Duplicate(AggregateRoot):
    def __init__(
        self,
        check_id: DuplicityCheckId,
        a_url: Url,
        another_url: Url,
        similarity: float,
    ):
        self._check_id = check_id
        self._a_url = a_url
        self._another_url = another_url
        self._similarity = similarity
        self._checked_on = datetime.now()

    @property
    def check_id(self) -> DuplicityCheckId:
        return self._check_id

    @property
    def url(self) -> Url:
        return self._a_url

    @property
    def duplicate_url(self) -> Url:
        return self._another_url

    @property
    def similarity(self) -> float:
        return self._similarity

    @property
    def checked_on(self) -> datetime:
        return self._checked_on


class DuplicateRepository(Repository, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def duplicates_since(self, since: datetime) -> List[Duplicate]:
        raise NotImplementedError

    @abc.abstractmethod
    def duplicates_of_check(self, check_id: DuplicityCheckId)\
            -> List[Duplicate]:
        raise NotImplementedError
