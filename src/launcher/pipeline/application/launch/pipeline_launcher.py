from dataclasses import dataclass, field
from typing import List

from shared.infrastructure.event import DomainEventPublisher
from launcher.shared.application.errors import MissingRequestParamsException
import shared.infrastructure.security as security
from shared.domain.user import User

from launcher.pipeline.domain.model.pipeline import Pipeline, PipelineId, PipelineRepository


@dataclass(frozen=True)
class PipelineLauncherCommand:
    sitemaps: list
    custom_request_headers: dict = field(default_factory={})
    selector_mapping: dict = field(default_factory={})
    excluded_tags: List[str] = field(default_factory=[])
    excluded_selectors: List[str] = field(default_factory=[])
    description: str = field(default=None)
    custom_fields: dict = field(default_factory={})
    url_address_pattern: str = None


class PipelineLauncher:
    def __init__(self, pipeline_repository: PipelineRepository):
        self._pipeline_repository = pipeline_repository

    @security.authorization_required('start:etl')
    def execute(self, user: User, command: PipelineLauncherCommand) -> PipelineId:
        CommandValidator.validate(command)

        pipeline = Pipeline(
            self._pipeline_repository.generate_identifier(),
            user.tenant_id(),
            self._pipeline_repository.generate_unique_name(),
            user.username(),
            command.sitemaps,
            command.description,
            command.custom_request_headers,
            command.selector_mapping,
            command.excluded_tags,
            command.excluded_selectors,
            command.url_address_pattern,
            command.custom_fields
        )

        self._pipeline_repository.add(pipeline)

        DomainEventPublisher.publish(pipeline.events())

        return pipeline.id


class CommandValidator:
    @staticmethod
    def validate(command: PipelineLauncherCommand):
        if not command.sitemaps:
            raise MissingRequestParamsException(
                "Parameter 'sitemapUrl' must be provided."
            )
