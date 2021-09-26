from dataclasses import dataclass
from shared.domain.bus.query import Response, Query, QueryHandler

from duplicates.report.domain.model.report import ReportRepository


@dataclass(frozen=True)
class NextIdentityQuery(Query):
    pass


@dataclass(frozen=True)
class NextIdentityResponse(Response):
    report_id: str


class NextIdentityQueryHandler(QueryHandler):
    def __init__(self, report_repository: ReportRepository):
        self._report_repository = report_repository

    def handle(self, query: NextIdentityQuery) -> NextIdentityResponse:
        next_identity = self._report_repository.next_identity()

        return NextIdentityResponse(report_id=next_identity.value)
