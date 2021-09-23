from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass
from shared.domain.bus.query import Response, Query, QueryHandler

from corpus_builder.shared.domain.model.tenant_id import TenantId
from corpus_builder.build.domain.model.build import BuildId, BuildStatus
from corpus_builder.build.domain.service.status.build_status_checker import BuildStatusChecker


@dataclass(frozen=True)
class StatusCheckerQuery(Query):
    build_id: str
    tenant_id: str


class StatusCheckerResponse(Response):
    def __init__(
        self,
        build_id: str,
        total_pages: int,
        pages_requested: int,
        started_on: datetime,
        is_completed: bool
    ):
        self._build_id = build_id
        self._total_pages = total_pages
        self._pages_requested = pages_requested
        self._started_on = started_on
        self._is_completed = is_completed

    @classmethod
    def from_value(cls, build_status: BuildStatus) -> StatusCheckerResponse:
        return cls(
            build_status.build_id,
            build_status.total_pages,
            build_status.requested_pages,
            build_status.build_started_on,
            build_status.is_completed
        )


class StatusCheckerQueryHandler(QueryHandler):
    def __init__(self, build_status_checker: BuildStatusChecker):
        self._build_status_checker = build_status_checker

    def handle(self, query: StatusCheckerQuery) -> StatusCheckerResponse:

        build_status = self._build_status_checker.retrieve_status(
            TenantId(query.tenant_id),
            BuildId(query.build_id)
        )

        return StatusCheckerResponse.from_value(build_status)
