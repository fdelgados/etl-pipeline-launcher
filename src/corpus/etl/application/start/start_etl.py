from dataclasses import dataclass, field
from typing import List

from shared import MissingRequestParamsException
from shared.infrastructure.event import DomainEventPublisher
from shared.domain.model.user.user import User

from corpus.etl.domain.model.etl import Etl, EtlId, EtlRepository


@dataclass(frozen=True)
class EtlStarterCommand:
    tenant_id: str
    username: str
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

    def start(self, command: EtlStarterCommand) -> EtlId:
        CommandValidator.validate(command)

        etl = Etl(
            self._etl_repository.generate_identifier(),
            command.tenant_id,
            self._etl_repository.generate_unique_name(),
            command.username,
            command.sitemaps,
            command.description,
            command.custom_request_headers,
            command.selector_mapping,
            command.excluded_tags,
            command.excluded_selectors,
            command.url_address_pattern,
            command.custom_fields,
        )

        self._etl_repository.save(etl)

        DomainEventPublisher.publish(etl.events())

        return etl.id


class CommandValidator:
    @staticmethod
    def validate(command: EtlStarterCommand):
        if not command.sitemaps:
            raise MissingRequestParamsException(
                "Parameter 'sitemapUrl' must be provided."
            )
