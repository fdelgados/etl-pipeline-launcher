from typing import Optional
from shared.domain.bus.query import Response, Query, QueryHandler


class StatusChecker(QueryHandler):
    def handle(self, query: Query) -> Optional[Response]:
        pass
