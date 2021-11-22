from __future__ import annotations

from typing import List

from dataclasses import dataclass, field

from datetime import datetime

from shared.domain.bus.query import Response, Query, QueryHandler
from shared.domain.bus.command import Command, CommandHandler
from shared.domain.errors.errors import Errors, ApplicationError

from shared.domain.bus.event import EventBus

from corpus.build.domain.model.build import (
    Build,
    BuildId,
    BuildRepository,
)
from corpus.build.domain.service.requests_counter import RequestsCounter


@dataclass(frozen=True)
class BuildingProgressQuery(Query):
    tenant_id: str
    build_id: str


class BuildingProgressResponse(Response):
    def __init__(self, build_dto: BuildDto):
        self._build_dto = build_dto

    def value(self) -> BuildDto:
        return self._build_dto


class BuildingProgressQueryHandler(QueryHandler):
    def __init__(
        self,
        build_repository: BuildRepository,
        requests_counter: RequestsCounter,
    ):
        self._build_repository = build_repository
        self._assembler = BuildAssembler(requests_counter)

    def handle(self, query: BuildingProgressQuery) -> BuildingProgressResponse:
        build = self._retrieve_build(query.tenant_id, BuildId(query.build_id))

        return BuildingProgressResponse(self._assembler.assemble(build))

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


@dataclass(frozen=True)
class BuildListQuery(Query):
    tenant_id: str


class BuildListResponse(Response):
    def __init__(self):
        self._build_dtos = []

    def add_dto(self, build_dto: BuildDto) -> None:
        self._build_dtos.append(build_dto)

    def value(self) -> List[BuildDto]:
        return self._build_dtos


class BuildListQueryHandler(QueryHandler):
    def __init__(
        self,
        build_repository: BuildRepository,
        requests_counter: RequestsCounter,
    ):
        self._build_repository = build_repository
        self._assembler = BuildAssembler(requests_counter)

    def handle(self, query: BuildListQuery) -> BuildListResponse:
        builds = self._build_repository.builds_of_tenant(query.tenant_id)

        response = BuildListResponse()

        for build in builds:
            response.add_dto(self._assembler.assemble(build))

        return response


@dataclass(frozen=True)
class BuildDto:
    build_id: str
    corpus_name: str
    total_requests: int
    failed_requests: int
    successful_requests: int
    started_on: datetime
    started_by: str
    completed_on: datetime
    status: dict = field(default_factory={})


class BuildAssembler:
    def __init__(self, requests_counter: RequestsCounter):
        self._requests_counter = requests_counter

    def assemble(self, build: Build) -> BuildDto:
        count_successful = build.successful_requests
        count_failed = build.failed_requests

        if not build.is_completed:
            count_successful = self._requests_counter.count_successful(
                build.id
            )
            count_failed = self._requests_counter.count_failed(build.id)

        return BuildDto(
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


@dataclass(frozen=True)
class NextIdentityQuery(Query):
    pass


class NextIdentityResponse(Response):
    def __init__(self, build_id: str):
        self._build_id = build_id

    def value(self) -> str:
        return self._build_id


class NextIdentityQueryHandler(QueryHandler):
    def __init__(self, build_repository: BuildRepository):
        self._build_repository = build_repository

    def handle(self, query: NextIdentityQuery) -> Response:
        build_id = self._build_repository.generate_identifier()

        response = NextIdentityResponse(build_id.value)

        return response


@dataclass(frozen=True)
class StartBuildCommand(Command):
    id: str
    tenant_id: str
    username: str
    corpus_name: str


class StartBuildCommandHandler(CommandHandler):
    def __init__(self, build_repository: BuildRepository, event_bus: EventBus):
        self._build_repository = build_repository
        self._event_bus = event_bus

    def handle(self, command: StartBuildCommand) -> None:
        CommandValidator.validate(command)

        running_builds = self._build_repository.running_builds_of_tenant(
            command.tenant_id
        )

        if running_builds:
            raise ApplicationError(
                Errors.conflict_error(
                    message="There are already running builds right now"
                )
            )

        build = Build(
            BuildId(command.id),
            command.tenant_id,
            self._build_repository.generate_unique_name(),
            command.username,
            command.corpus_name,
        )

        self._build_repository.save(build)

        self._event_bus.publish(*build.pull_events())


class CommandValidator:
    @staticmethod
    def validate(command: StartBuildCommand):
        if not command.corpus_name:
            raise ApplicationError(Errors.missing_request_parameter())
