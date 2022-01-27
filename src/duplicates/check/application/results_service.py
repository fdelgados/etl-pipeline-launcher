from __future__ import annotations

from typing import List

from dataclasses import dataclass
from datetime import datetime

from shared.domain.bus.query import Query, QueryHandler, Response
from shared.infrastructure.utils.json_serializable import JsonSerializable

from duplicates.check.domain.model.duplicate import (
    DuplicateRepository,
    Duplicate,
)

from duplicates.check.domain.model.duplicitycheck import (
    DuplicityCheckId,
    DuplicityCheckRepository,
    Status,
)


@dataclass(frozen=True)
class RetrieveDuplicityCheckResultsQuery(Query):
    since: str = ""
    check_id: str = ""


class RetrieveDuplicityCheckResultsResponse(Response):
    def __init__(self, duplicates_dto: DuplicatesDto):
        self._duplicates_dto = duplicates_dto

    def value(self) -> DuplicatesDto:
        return self._duplicates_dto


class RetrieveDuplicityCheckResultsQueryHandler(QueryHandler):
    def __init__(
        self,
        duplicate_repository: DuplicateRepository,
        duplicity_check_repository: DuplicityCheckRepository,
    ):
        self._duplicate_repository = duplicate_repository
        self._duplicity_check_repository = duplicity_check_repository

    def handle(
        self, query: RetrieveDuplicityCheckResultsQuery
    ) -> RetrieveDuplicityCheckResultsResponse:
        dto = DuplicatesDto()
        duplicates = []

        if query.since:
            since = datetime.fromisoformat(query.since)

            duplicates = self._duplicate_repository.duplicates_since(since)

        if query.check_id:
            check_id = DuplicityCheckId(query.check_id)
            duplicity_check = (
                self._duplicity_check_repository.duplicity_check_of_id(
                    check_id
                )
            )
            dto.status = duplicity_check.status.serialize()

            if duplicity_check.status == Status.completed():
                dto.mark_process_as_completed()
                duplicates = self._duplicate_repository.duplicates_of_check(
                    check_id
                )

        for duplicate in duplicates:
            dto.add_duplicate(
                duplicate.check_id.value,
                duplicate.url.address,
                duplicate.duplicate_url.address,
                duplicate.similarity,
                duplicate.checked_on,
            )

        return RetrieveDuplicityCheckResultsResponse(dto)

    def _find_duplicates(self, query) -> List[Duplicate]:
        if query.since:
            since = datetime.fromisoformat(query.since)

            return self._duplicate_repository.duplicates_since(since)

        if query.check_id:
            check_id = DuplicityCheckId(query.check_id)
            duplicity_check = (
                self._duplicity_check_repository.duplicity_check_of_id(
                    check_id
                )
            )

            if duplicity_check.status == Status.in_progress():
                return []

            return self._duplicate_repository.duplicates_of_check(check_id)

    def _find_duplicates_since(self, since: str) -> List[Duplicate]:
        return self._duplicate_repository.duplicates_since(
            datetime.fromisoformat(since)
        )


class DuplicatesDto(JsonSerializable):
    def __init__(self):
        self._duplicates = []
        self._status = None
        self._process_completed = False

    def add_duplicate(
        self,
        check_id: str,
        url: str,
        duplicated_url: str,
        similarity: float,
        checked_on: datetime,
    ):
        duplicate = {
            "url": duplicated_url,
            "similarity": similarity,
            "checked_on": checked_on,
            "check_id": check_id,
        }

        existing_url_index = next(
            (
                index
                for (index, d) in enumerate(self._duplicates)
                if d["url"] == url
            ),
            None,
        )

        if existing_url_index is None:
            self._duplicates.append({"url": url, "duplicates": [duplicate]})
        else:
            self._duplicates[existing_url_index]["duplicates"].append(
                duplicate
            )

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, status: str) -> None:
        self._status = status

    def mark_process_as_completed(self) -> None:
        self._process_completed = True

    def is_process_completed(self) -> bool:
        return self._process_completed

    def serialize(self) -> list:
        return self._duplicates
