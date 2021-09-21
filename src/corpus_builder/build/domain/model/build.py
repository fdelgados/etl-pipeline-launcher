from __future__ import annotations

import abc

from coolname import generate

from shared_context.domain.model import AggregateRoot, Uuid, Repository
from corpus_builder.build.domain.event.build_started import BuildStarted
from corpus_builder.build.domain.event.build_completed import BuildCompleted


__all__ = ["BuildId", "Build", "BuildRepository"]


class BuildId(Uuid):
    pass


class Build(AggregateRoot):
    def __init__(
        self,
        build_id: BuildId,
        tenant_id: str,
        name: str,
        started_by: str,
        corpus_name: str
    ):
        self._build_id = build_id
        self._tenant_id = tenant_id
        self._started_by = started_by
        self._name = name
        self._corpus_name = corpus_name
        self._total_pages = 0
        self._completed = False
        self._completed_on = None

        event = BuildStarted(
            self._tenant_id,
            self._build_id.value,
            self._name,
            self._started_by,
            self._corpus_name
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
        return self._completed

    @property
    def total_pages(self) -> int:
        return self._total_pages

    @total_pages.setter
    def total_pages(self, total_pages: int) -> None:
        self._total_pages = total_pages

    def complete(self) -> None:
        build_completed = BuildCompleted(self._tenant_id, self._build_id.value)

        self.record_event(build_completed)

        self._completed = True
        self._completed_on = build_completed.occurred_on

    def __repr__(self):
        return "Build <{}>".format(self._build_id.value)


class BuildRepository(Repository, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def build_of_tenant_and_id(self, tenant_id: str, build_id: BuildId):
        raise NotImplementedError

    @staticmethod
    def generate_identifier() -> BuildId:
        return BuildId()

    @staticmethod
    def generate_unique_name() -> str:
        return " ".join(x.capitalize() for x in generate(2))
