from dataclasses import dataclass

from shared.domain.bus.command import Command, CommandHandler

from shared.domain.bus.event import EventBus
from shared.domain.errors.errors import Errors, ApplicationError

from corpus.build.domain.model.build import Build, BuildId, BuildRepository


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
