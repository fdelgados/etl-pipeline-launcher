from dataclasses import dataclass, field
from typing import List

from shared.infrastructure.event import DomainEventPublisher
from launcher.shared.application.errors import MissingRequestParamsException
import shared.infrastructure.security as sec
from shared.domain.user import User

from launcher.pipeline.domain.model import Pipeline, PipelineId, PipelineRepository
from launcher.pipeline.domain.event import PipelineLaunched


@dataclass(frozen=True)
class LaunchPipelineCommand:
    sitemap_url: str
    custom_request_headers: dict = field(default_factory={})
    selector_mapping: dict = field(default_factory={})
    excluded_selectors: List[str] = field(default_factory=[])
    description: str = field(default=None)
    custom_fields: dict = field(default_factory={})


class LaunchPipeline:
    def __init__(self, pipeline_repository: PipelineRepository):
        self._pipeline_repository = pipeline_repository

    @sec.authorization_required('start:etl')
    def execute(self, user: User, command: LaunchPipelineCommand) -> PipelineId:
        CommandValidator.validate(command)

        pipeline = Pipeline(
            self._pipeline_repository.generate_identifier(),
            user.tenant_id(),
            user.username()
        )

        self._pipeline_repository.add(pipeline)

        pipeline_launched = PipelineLaunched(
            pipeline.tenant_id,
            str(pipeline.pipeline_id),
            command.custom_request_headers,
            command.selector_mapping,
            command.excluded_selectors,
            command.sitemap_url,
            command.description,
            command.custom_fields
        )

        DomainEventPublisher.publish([pipeline_launched])

        return pipeline.pipeline_id


class CommandValidator:
    @staticmethod
    def validate(command: LaunchPipelineCommand):
        if not command.sitemap_url:
            raise MissingRequestParamsException(
                "Parameter 'sitemapUrl' must be provided."
            )
