from __future__ import annotations

import abc

from typing import Dict


class MinHash:
    def __init__(self, value):
        self._value = value

    def jaccard(self, minhash: MinHash):
        return self._value.jaccard(minhash.value)

    @property
    def value(self):
        return self._value


class MinHashRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_all_of_tenant(self, tenant_id: str, minhashes: Dict[str, MinHash]):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_of_tenant(self, tenant_id: str) -> Dict[str, MinHash]:
        raise NotImplementedError
