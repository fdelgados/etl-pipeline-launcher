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

from duplicates.check.domain.model.duplicitycheck import DuplicityCheckId


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
    def __init__(self, duplicate_repository: DuplicateRepository):
        self._duplicate_repository = duplicate_repository

    def handle(self, query: RetrieveDuplicityCheckResultsQuery) \
            -> RetrieveDuplicityCheckResultsResponse:

        duplicates = self._find_duplicates(query)

        dto = DuplicatesDto()

        for duplicate in duplicates:
            dto.add_duplicate(
                duplicate.check_id.value,
                duplicate.url.address,
                duplicate.duplicate_url.address,
                duplicate.similarity,
                duplicate.checked_on
            )

        return RetrieveDuplicityCheckResultsResponse(dto)

    def _find_duplicates(self, query) -> List[Duplicate]:
        if query.since:
            since = datetime.fromisoformat(query.since)

            return self._duplicate_repository.duplicates_since(since)

        if query.check_id:
            check_id = DuplicityCheckId(query.check_id)

            return self._duplicate_repository.duplicates_of_check(check_id)


class DuplicatesDto(JsonSerializable):
    def __init__(self):
        self._duplicates = []
        self._already_listed = []

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
            (index for (index, d) in enumerate(self._duplicates)
                if d["url"] == url),
            None
        )

        if existing_url_index is None:
            self._duplicates.append(
                {
                    "url": url,
                    "duplicates": [duplicate]
                }
            )
        else:
            self._duplicates[existing_url_index]["duplicates"].append(
                duplicate
            )

    def serialize(self) -> list:
        return self._duplicates

