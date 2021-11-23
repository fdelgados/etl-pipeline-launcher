from __future__ import annotations

import abc

from duplicates.similarity.domain.event.duplicitydetected import (
    DuplicityDetected,
)
from duplicates.report.domain.model.report import ReportId
from shared.domain.model.valueobject.url import Url
from shared.domain.model.aggregate import AggregateRoot
from shared.domain.model.repository import Repository


class Duplicate(AggregateRoot):
    def __init__(
        self,
        report_id: ReportId,
        a_url: Url,
        another_url: Url,
        similarity: float,
    ):
        self._report_id = report_id
        self._a_url = a_url
        self._another_url = another_url
        self._similarity = similarity

        self.record_event(
            DuplicityDetected(
                self._report_id.value,
                self._a_url.address,
                self._another_url.address,
                self._similarity,
            )
        )


class DuplicateRepository(Repository, metaclass=abc.ABCMeta):
    pass
