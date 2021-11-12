from dataclasses import dataclass, field, asdict

from typing import List

from datetime import datetime

from shared.domain.bus.query import Response, Query, QueryHandler
from shared.domain.errors.errors import Errors, ApplicationError

from corpus.build.domain.model.build import (
    Build,
    BuildId,
    BuildRepository,
)
from corpus.build.domain.service.requests_counter import RequestsCounter


@dataclass(frozen=True)
class RetrieveBuildInfoQuery(Query):
    tenant_id: str
    build_id: str = field(default=None)


@dataclass(frozen=True)
class BuildInfoDto:
    build_id: str
    corpus_name: str
    total_requests: int
    failed_requests: int
    successful_requests: int
    started_on: datetime
    started_by: str
    completed_on: datetime
    status: dict = field(default_factory={})

    def to_dict(self):
        return asdict(self)


class RetrieveBuildInfoResponse(Response):
    def __init__(self):
        self._build_info_dtos: List[BuildInfoDto] = []

    @property
    def build_info_dtos(self) -> List[BuildInfoDto]:
        return self._build_info_dtos

    def add_dto(self, build_info_dto: BuildInfoDto) -> None:
        self._build_info_dtos.append(build_info_dto)


class RetrieveBuildInfoQueryHandler(QueryHandler):
    def __init__(
        self,
        build_repository: BuildRepository,
        requests_counter: RequestsCounter,
    ):
        self._build_repository = build_repository
        self._requests_counter = requests_counter

    def handle(
        self, query: RetrieveBuildInfoQuery
    ) -> RetrieveBuildInfoResponse:

        response = RetrieveBuildInfoResponse()
        if query.build_id:
            build = self._retrieve_build(
                query.tenant_id, BuildId(query.build_id)
            )

            self._add_dto(response, build)

            return response

        builds = self._build_repository.builds_of_tenant(query.tenant_id)
        if not builds:
            raise ApplicationError(
                Errors.entity_not_found(entity_name="Build")
            )

        for build in builds:
            self._add_dto(response, build)

        return response

    def _retrieve_build(self, tenant_id: str, build_id: BuildId) -> Build:
        build = self._build_repository.build_of_tenant_and_id(
            tenant_id, build_id
        )

        if not build:
            raise ApplicationError(
                Errors.entity_not_found(
                    entity_name="Build", entity_id=build_id.value
                )
            )

        return build

    def _add_dto(
        self, response: RetrieveBuildInfoResponse, build: Build
    ) -> None:
        count_successful = build.successful_requests
        count_failed = build.failed_requests

        if not build.is_completed:
            count_successful = self._requests_counter.count_successful(
                build.id
            )
            count_failed = self._requests_counter.count_failed(build.id)

        build_info_dto = BuildInfoDto(
            build.id.value,
            build.corpus_name,
            build.total_requests,
            count_failed,
            count_successful,
            build.started_on,
            build.started_by,
            build.completed_on,
            build.status.serialize(),
        )

        response.add_dto(build_info_dto)
