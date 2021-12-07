from typing import List

from shared.domain.bus.event import DomainEvent


class DuplicityCheckRequested(DomainEvent):
    def __init__(
        self,
        tenant_id: str,
        check_id: str,
        urls: List[str],
        similarity_threshold: float,
        requested_by: str,
        corpus: str,
    ):
        super().__init__(check_id)

        self._tenant_id = tenant_id
        self._check_id = check_id
        self._urls = urls
        self._similarity_threshold = similarity_threshold
        self._requested_by = requested_by
        self._corpus = corpus

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def check_id(self) -> str:
        return self._check_id

    @property
    def urls(self) -> List[str]:
        return self._urls

    @property
    def similarity_threshold(self) -> float:
        return self._similarity_threshold

    @property
    def requested_by(self) -> str:
        return self._requested_by

    @property
    def corpus(self) -> str:
        return self._corpus
