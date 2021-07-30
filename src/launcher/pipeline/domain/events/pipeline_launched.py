from __future__ import annotations

from typing import Dict, List

from shared_context.domain.events import DomainEvent
from launcher.pipeline.domain.model.aggregate import TenantId, PipelineId


class PipelineLaunched(DomainEvent):
    def __init__(
        self, tenant_id: TenantId,
        pipeline_id: PipelineId,
        custom_request_headers: Dict,
        selector_mapping: Dict,
        excluded_selectors: List,
        sitemap_url: str,
        description: str,
        custom_fields: Dict
    ):
        super().__init__()

        self.tenant_id = tenant_id
        self.pipeline_id = pipeline_id
        self.custom_request_headers = custom_request_headers
        self.selector_mapping = selector_mapping
        self.excluded_selectors = excluded_selectors
        self.sitemap_url = sitemap_url
        self.description = description
        self.custom_fields = custom_fields
