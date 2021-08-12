from dataclasses import dataclass, field
from typing import List

from shared_context.application import Command, CommandHandler
from shared_context.domain.events import DomainEventPublisher

from shared.application.errors import InvalidRequestParamsException, ErrorCodes

from launcher.pipeline.domain.model.aggregate import Pipeline, PipelineId
from launcher.pipeline.domain.model.repository import PipelineRepository
from launcher.pipeline.domain.events.pipeline_launched import PipelineLaunched
from launcher.tenant.domain.model.aggregate import TenantId
from launcher.tenant.domain.service.finder import TenantFinder


@dataclass(frozen=True)
class LaunchPipelineCommand(Command):
    tenant_id: str
    sitemap_url: str
    custom_request_headers: dict = field(default_factory={})
    selector_mapping: dict = field(default_factory={})
    excluded_selectors: List[str] = field(default_factory=[])
    description: str = field(default=None)
    custom_fields: dict = field(default_factory={})


class LaunchPipeline(CommandHandler):
    def __init__(
        self,
        pipeline_repository: PipelineRepository,
        tenant_finder: TenantFinder
    ):
        self._pipeline_repository = pipeline_repository
        self._tenant_finder = tenant_finder

    def handle(self, command: LaunchPipelineCommand) -> PipelineId:
        CommandValidator.validate(command)

        try:
            tenant_id = TenantId(command.tenant_id)
        except ValueError as e:
            raise InvalidRequestParamsException(
                ErrorCodes.INVALID_REQUEST_PARAMETER,
                str(e)
            )

        tenant = self._tenant_finder.find(tenant_id)

        pipeline = Pipeline(
            self._pipeline_repository.generate_identifier(),
            tenant.id
        )

        self._pipeline_repository.add(pipeline)

        pipeline_launched = PipelineLaunched(
            pipeline.tenant_id,
            pipeline.pipeline_id,
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
        if not command.tenant_id:
            raise InvalidRequestParamsException(
                ErrorCodes.MISSING_REQUEST_PARAMETER,
                "Tenant must be provided"
            )

        if not command.sitemap_url:
            raise InvalidRequestParamsException(
                ErrorCodes.MISSING_REQUEST_PARAMETER,
                "Parameter 'sitemapUrl' must be provided."
            )
