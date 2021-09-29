from dataclasses import dataclass
from typing import Optional
from shared.domain.bus.query import Response, Query, QueryHandler

from corpus.build.domain.model.build import BuildRepository


@dataclass(frozen=True)
class NextIdentityQuery(Query):
    pass


@dataclass(frozen=True)
class NextIdentityResponse(Response):
    build_id: str


class NextIdentityQueryHandler(QueryHandler):
    def __init__(self, build_repository: BuildRepository):
        self._build_repository = build_repository

    def handle(self, query: NextIdentityQuery) -> Optional[Response]:
        next_identity = self._build_repository.generate_identifier()

        return NextIdentityResponse(build_id=next_identity.value)
