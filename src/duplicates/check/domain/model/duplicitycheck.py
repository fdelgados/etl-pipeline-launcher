from __future__ import annotations

import abc

from datetime import datetime

from typing import List, Optional

from shared.domain.model.entity.user import User
from shared.domain.model.aggregate import AggregateRoot
from shared.domain.model.repository import Repository
from shared.domain.model.valueobject.url import Url
from shared.domain.model.valueobject.uid import Uuid
from duplicates.shared.domain.model.similarity_threshold import (
    SimilarityThreshold,
)
from duplicates.check.domain.event.duplicitycheckrequested import (
    DuplicityCheckRequested,
)


class DuplicityCheckId(Uuid):
    pass


class Status:
    _IN_PROGRESS = 0
    _COMPLETED = 1

    _STATUS = {
        _IN_PROGRESS: "In progress",
        _COMPLETED: "Completed",
    }

    def __init__(self, value: int):
        self._value = value
        self._description = self._STATUS[self._value]

    @property
    def value(self) -> int:
        return self._value

    @classmethod
    def in_progress(cls) -> Status:
        return cls(cls._IN_PROGRESS)

    @classmethod
    def completed(cls) -> Status:
        return cls(cls._COMPLETED)

    def complete(self) -> Status:
        return Status(self._COMPLETED)

    def serialize(self) -> dict:
        return {"id": self._value, "description": self._description}

    def __repr__(self):
        return self.serialize()

    def __eq__(self, other):
        if not isinstance(other, Status):
            return False

        return other.value == self.value


class DuplicityCheck(AggregateRoot):
    def __init__(
        self,
        check_id: DuplicityCheckId,
        urls: List[Url],
        similarity_threshold: SimilarityThreshold,
        requested_by: User,
        corpus: str,
    ):
        self._id = check_id
        self._urls = urls
        self._similarity_threshold = similarity_threshold
        self._requested_by = requested_by.username()
        self._tenant_id = requested_by.tenant_id()
        self._completed_on = None
        self._status = Status.in_progress()
        self._corpus = corpus

        event = DuplicityCheckRequested(
            self._tenant_id,
            self._id.value,
            [url.address for url in urls],
            self._similarity_threshold.value,
            self._requested_by,
            self._corpus,
        )

        self._requested_on = event.occurred_on

        self.record_event(event)

    @property
    def id(self) -> DuplicityCheckId:
        return self._id

    @property
    def urls(self) -> List[Url]:
        return self._urls

    @property
    def similarity_threshold(self) -> SimilarityThreshold:
        return self._similarity_threshold

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def requested_by(self) -> str:
        return self._requested_by

    @property
    def requested_on(self) -> datetime:
        return self._requested_on

    def complete(self) -> None:
        self._status = self._status.complete()
        self._completed_on = datetime.now()

    @property
    def completed_on(self) -> Optional[datetime]:
        return self._completed_on

    @property
    def status(self) -> Status:
        return self._status

    @property
    def corpus(self) -> str:
        return self._corpus


class DuplicityCheckRepository(Repository, metaclass=abc.ABCMeta):
    @staticmethod
    def next_identity() -> DuplicityCheckId:
        return DuplicityCheckId()

    @abc.abstractmethod
    def duplicity_check_of_id(self, duplicity_check_id)\
            -> Optional[DuplicityCheck]:
        raise NotImplementedError


class Duplicate:
    def __init__(
        self,
        check_id: DuplicityCheckId,
        a_url: Url,
        another_url: Url,
        similarity: float,
    ):
        self._report_id = check_id
        self._a_url = a_url
        self._another_url = another_url
        self._similarity = similarity
        self._checked_on = datetime.now()
