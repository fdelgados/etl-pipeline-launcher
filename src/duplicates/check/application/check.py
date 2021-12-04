from dataclasses import dataclass
from shared.domain.bus.command import Command, CommandHandler


@dataclass(frozen=True)
class CheckDuplicationCommand(Command):
    content: str
    similarity_threshold: float


class CheckDuplicationCommandHandler(CommandHandler):
    def handle(self, command: CheckDuplicationCommand) -> None:
        pass
