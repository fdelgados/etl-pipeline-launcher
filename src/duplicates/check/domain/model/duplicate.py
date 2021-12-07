import abc

from datetime import datetime

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


class DuplicateRepository(Repository, metaclass=abc.ABCMeta):
    pass
