from dataclasses import dataclass, field
from typing import List

from shared import MissingRequestParamsException
from shared.infrastructure.event import DomainEventPublisher
from shared.infrastructure.security import authorization_required
from shared.domain.model.user.user import User

from corpus.etl.domain.model.etl import Etl, EtlId, EtlRepository


@dataclass(frozen=True)
class EtlStarterCommand:
    sitemaps: list
    custom_request_headers: dict = field(default_factory={})
    selector_mapping: dict = field(default_factory={})
    excluded_tags: List[str] = field(default_factory=[])
    excluded_selectors: List[str] = field(default_factory=[])
    description: str = field(default=None)
    custom_fields: dict = field(default_factory={})
    url_address_pattern: str = None


class EtlStarter:
    def __init__(self, etl_repository: EtlRepository):
        self._etl_repository = etl_repository

    @authorization_required("start:etl")
    def start(self, user: User, command: EtlStarterCommand) -> EtlId:
        CommandValidator.validate(command)

        etl = Etl(
            self._etl_repository.generate_identifier(),
            user.tenant_id(),
            self._etl_repository.generate_unique_name(),
            user.username(),
            command.sitemaps,
            command.description,
            command.custom_request_headers,
            command.selector_mapping,
            command.excluded_tags,
            command.excluded_selectors,
            command.url_address_pattern,
            command.custom_fields,
        )

        self._etl_repository.add(etl)

        DomainEventPublisher.publish(etl.events())

        return etl.id


class CommandValidator:
    @staticmethod
    def validate(command: EtlStarterCommand):
        if not command.sitemaps:
            raise MissingRequestParamsException(
                "Parameter 'sitemapUrl' must be provided."
            )
