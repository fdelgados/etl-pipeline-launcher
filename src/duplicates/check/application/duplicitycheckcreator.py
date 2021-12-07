from dataclasses import dataclass

from typing import List

from shared.domain.bus.command import Command, CommandHandler
from shared.domain.bus.event import EventBus
from shared.domain.model.entity.user import User
from shared.domain.model.valueobject.url import Url, InvalidUrlException
from shared.domain.errors.errors import Errors, ApplicationError

from duplicates.shared.domain.model.similarity_threshold import (
    SimilarityThreshold,
)
from duplicates.check.domain.model.duplicitycheck import (
    DuplicityCheckRepository,
    DuplicityCheck,
)


@dataclass(frozen=True)
class CreateDuplicityCheckCommand(Command):
    urls: list
    similarity_threshold: float
    requested_by: User
    corpus: str


def _sanitize_urls(addresses: list) -> List[Url]:
    urls = []

    for address in set(addresses):
        try:
            urls.append(Url(address))
        except InvalidUrlException:
            continue

    return urls


class CreateDuplicityCheckCommandHandler(CommandHandler):
    _MAX_URLS_TO_CHECK = 100

    def __init__(
        self,
        duplicity_check_repository: DuplicityCheckRepository,
        event_bus: EventBus,
    ):
        self._duplicity_check_repository = duplicity_check_repository
        self._event_bus = event_bus

    def handle(self, command: CreateDuplicityCheckCommand) -> None:
        urls = _sanitize_urls(command.urls)

        self._ensure_max_urls_is_not_exceeded(urls)

        duplicity_check = DuplicityCheck(
            self._duplicity_check_repository.next_identity(),
            urls,
            SimilarityThreshold(command.similarity_threshold),
            command.requested_by,
            command.corpus,
        )

        self._duplicity_check_repository.save(duplicity_check)

        self._event_bus.publish(*duplicity_check.pull_events())

    def _ensure_max_urls_is_not_exceeded(self, urls: List[Url]) -> None:
        if len(urls) > self._MAX_URLS_TO_CHECK:
            error = Errors.limit_exceeded(
                details="Maximum number of URLs exceeded. {} allowed".format(
                    self._MAX_URLS_TO_CHECK
                )
            )

            raise ApplicationError(error)
