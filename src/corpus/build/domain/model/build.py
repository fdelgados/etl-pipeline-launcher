from __future__ import annotations

import abc

from typing import Optional, List

from datetime import datetime
from coolname import generate

from shared.domain.model.aggregate import AggregateRoot
from shared.domain.model.value_object.unique_id import Uuid
from shared.domain.model.repository import Repository
from corpus.build.domain.event.build_started import BuildStarted
from corpus.build.domain.event.build_completed import BuildCompleted
from corpus.build.domain.event.build_aborted import BuildAborted
from corpus.build.domain.event.build_cancelled import BuildCancelled


class BuildId(Uuid):
    pass


class Status:
    _CANCELLED = -2
    _ABORTED = -1
    _RUNNING = 0
    _COMPLETED = 1

    _STATUS = {
        _CANCELLED: "Cancelled by user",
        _ABORTED: "Aborted due to an error",
        _RUNNING: "Running",
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

    def is_completed(self) -> bool:
        return self.value == self._COMPLETED

    def is_running(self) -> bool:
        return self.value == self._RUNNING

    def is_cancelled(self) -> bool:
        return self.value == self._CANCELLED

    def is_aborted(self) -> bool:
        return self.value == self._ABORTED

    @classmethod
    def running(cls) -> Status:
        return cls(cls._RUNNING)

    @classmethod
    def completed(cls) -> Status:
        return cls(cls._COMPLETED)

    @classmethod
    def cancelled(cls) -> Status:
        return cls(cls._CANCELLED)

    @classmethod
    def aborted(cls) -> Status:
        return cls(cls._ABORTED)

    def __dict__(self):
        return self.serialize()

    def __eq__(self, other):
        if not isinstance(other, Status):
            return False

        return other.value == self.value


class Build(AggregateRoot):
    def __init__(
        self,
        build_id: BuildId,
        tenant_id: str,
        name: str,
        started_by: str,
        corpus_name: str,
    ):
        self._build_id = build_id
        self._tenant_id = tenant_id
        self._started_by = started_by
        self._name = name
        self._corpus_name = corpus_name
        self._total_requests = 0
        self._successful_requests = 0
        self._failed_requests = 0
        self._status = Status.running()
        self._completed_on = None

        event = BuildStarted(
            self._tenant_id,
            self._build_id.value,
            self._name,
            self._started_by,
            self._corpus_name,
        )
        self._started_on = event.occurred_on

        self.record_event(event)

    @property
    def id(self) -> BuildId:
        return self._build_id

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def corpus_name(self) -> str:
        return self._corpus_name

    @property
    def is_completed(self) -> bool:
        return self._status.is_completed()

    @property
    def started_on(self) -> datetime:
        return self._started_on

    @property
    def started_by(self) -> str:
        return self._started_by

    @property
    def total_requests(self) -> int:
        return self._total_requests

    @total_requests.setter
    def total_requests(self, total_requests: int) -> None:
        self._total_requests = total_requests

    @property
    def successful_requests(self) -> int:
        return self._successful_requests

    @successful_requests.setter
    def successful_requests(self, successful_requests: int) -> None:
        self._successful_requests = successful_requests

    @property
    def failed_requests(self) -> int:
        return self._failed_requests

    @failed_requests.setter
    def failed_requests(self, failed_requests: int) -> None:
        self._failed_requests = failed_requests

    def cancel(self) -> None:
        self._status = Status.cancelled()

        self.record_event(
            BuildCancelled(
                self._tenant_id,
                self._build_id.value,
                self._corpus_name,
            )
        )

    def abort(self) -> None:
        self._status = Status.aborted()

        self.record_event(
            BuildAborted(
                self._tenant_id,
                self._build_id.value,
                self._corpus_name,
            )
        )

    def complete(self) -> None:
        self._status = Status.completed()

        build_completed = BuildCompleted(
            self._tenant_id,
            self._build_id.value,
            self._corpus_name,
        )

        self.record_event(build_completed)

        self._completed_on = build_completed.occurred_on

    @property
    def completed_on(self) -> Optional[datetime]:
        return self._completed_on

    @property
    def status(self) -> Status:
        return self._status

    def __repr__(self):
        return "Build <{}>".format(self._build_id.value)


class BuildRepository(Repository, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def build_of_tenant_and_id(
        self, tenant_id: str, build_id: BuildId
    ) -> Optional[Build]:
        raise NotImplementedError

    @abc.abstractmethod
    def builds_of_tenant(self, tenant_id: str) -> List[Build]:
        raise NotImplementedError

    @staticmethod
    def generate_identifier() -> BuildId:
        return BuildId()

    @staticmethod
    def generate_unique_name() -> str:
        return " ".join(x.capitalize() for x in generate(2))
