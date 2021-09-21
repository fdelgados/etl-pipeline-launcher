from dataclasses import dataclass

from shared import MissingRequestParamsException
from shared.infrastructure.event import DomainEventDispatcher

from corpus_builder.build.domain.model.build import Build, BuildId, BuildRepository


@dataclass(frozen=True)
class BuildStarterCommand:
    tenant_id: str
    username: str
    corpus_name: str


class BuildStarter:
    def __init__(self, build_repository: BuildRepository):
        self._build_repository = build_repository

    def start(self, command: BuildStarterCommand) -> BuildId:
        CommandValidator.validate(command)

        build = Build(
            self._build_repository.generate_identifier(),
            command.tenant_id,
            self._build_repository.generate_unique_name(),
            command.username,
            command.corpus_name
        )

        self._build_repository.save(build)

        DomainEventDispatcher.dispatch(build.events())

        return build.id


class CommandValidator:
    @staticmethod
    def validate(command: BuildStarterCommand):
        if not command.corpus_name:
            raise MissingRequestParamsException(
                "Parameter 'sitemapUrl' must be provided."
            )
