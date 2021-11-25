from __future__ import annotations

import abc
from datetime import datetime
from typing import Optional

from coolname import generate

from shared.domain.model.valueobject.uid import Uuid
from shared.domain.model.aggregate import AggregateRoot
from shared.domain.model.repository import Repository
from shared.domain.model.entity.user import User
from duplicates.shared.domain.model.similarity_threshold import (
    SimilarityThreshold,
)
from duplicates.shared.domain.model.k_shingle_size import KShingleSize
from duplicates.report.domain.event.reportcreated import ReportCreated


class ReportId(Uuid):
    pass


class Status:
    _CANCELLED = -1
    _CREATED = 0
    _ANALYSIS_IN_PROGRESS = 1
    _COMPLETED = 2

    _STATUS = {
        _CREATED: "Created",
        _ANALYSIS_IN_PROGRESS: "Analysis in progress",
        _CANCELLED: "Cancelled",
        _COMPLETED: "Completed",
    }

    def __init__(self, value: int):
        self._value = value
        self._description = self._STATUS[self._value]

    @property
    def value(self):
        return self._value

    def serialize(self):
        return {"id": self._value, "description": self._description}

    @classmethod
    def created(cls) -> Status:
        return cls(cls._CREATED)

    def complete(self) -> Status:
        return Status(self._COMPLETED)

    def cancel(self) -> Status:
        return Status(self._CANCELLED)

    def analysis_in_progress(self) -> Status:
        return Status(self._ANALYSIS_IN_PROGRESS)

    def __dict__(self):
        return self.serialize()

    def __eq__(self, other):
        if not isinstance(other, Status):
            return False

        return other.value == self.value


class Report(AggregateRoot):
    def __init__(
        self,
        report_id: ReportId,
        name: str,
        from_corpus: str,
        creator: User,
        k_shingle_size: KShingleSize,
        similarity_threshold: SimilarityThreshold,
    ):
        self._report_id = report_id
        self._name = name
        self._from_corpus = from_corpus
        self._creator = creator
        self._created_by = self._creator.username()
        self._tenant_id = self._creator.tenant_id()
        self._k_shingle_size = k_shingle_size
        self._similarity_threshold = similarity_threshold
        self._completed_on = None
        self._total_pages = 0
        self._duplicated_pages = 0
        self._duplication_ratio = None
        self._duplication_average = None
        self._duplication_median = None
        self._completed = False
        self._status = Status.created()

        report_created = ReportCreated(
            self._report_id.value,
            self._name,
            self._from_corpus,
            self._created_by,
            self._tenant_id,
            self._k_shingle_size.value,
            self._similarity_threshold.value,
        )

        self._started_on = report_created.occurred_on

        self.record_event(report_created)

    @property
    def report_id(self) -> ReportId:
        return self._report_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def from_corpus(self) -> str:
        return self._from_corpus

    @property
    def created_by(self) -> str:
        return self._created_by

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def creator(self) -> User:
        return self._creator

    @property
    def k_shingle_size(self) -> KShingleSize:
        return self._k_shingle_size

    @property
    def similarity_threshold(self) -> SimilarityThreshold:
        return self._similarity_threshold

    @property
    def started_on(self) -> datetime:
        return self._started_on

    def complete(self) -> None:
        self._status = self._status.complete()
        self._completed_on = datetime.now()

    def start_analysis(self) -> None:
        self._status = self._status.analysis_in_progress()

    @property
    def is_completed(self) -> bool:
        return self._completed

    @property
    def completed_on(self) -> Optional[datetime]:
        return self._completed_on

    @property
    def status(self) -> Status:
        return self._status

    def cancel(self):
        self._status = self._status.cancel()

    @property
    def total_pages(self) -> int:
        return self._total_pages

    @total_pages.setter
    def total_pages(self, total_pages: int) -> None:
        self._total_pages = total_pages


class ReportRepository(Repository, metaclass=abc.ABCMeta):
    @staticmethod
    def next_identity() -> ReportId:
        return ReportId()

    @staticmethod
    def generate_unique_name() -> str:
        return " ".join(x.capitalize() for x in generate(2))

    @abc.abstractmethod
    def report_of_id(self, report_id: ReportId) -> Optional[Report]:
        raise NotImplementedError
