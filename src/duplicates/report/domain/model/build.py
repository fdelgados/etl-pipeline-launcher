import abc

from datetime import datetime


class Build:
    def __init__(self, build_id: str, build_name: str, created_on: datetime):
        self._build_id = build_id
        self._build_name = build_name
        self._created_on = created_on

    @property
    def id(self) -> str:
        return self._build_id

    @property
    def name(self) -> str:
        return self._build_name


class BuildRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def last_build(self, tenant_id: str, corpus_name: str) -> Build:
        raise NotImplementedError
