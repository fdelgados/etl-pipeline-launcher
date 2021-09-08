from __future__ import annotations

import abc

from typing import Dict, Optional, List
from datetime import datetime
from coolname import generate

from shared_context.domain.model import AggregateRoot, Uuid, Repository
from launcher.pipeline.domain.event.pipeline_launched import PipelineLaunched


class PipelineId(Uuid):
    pass


class Pipeline(AggregateRoot):
    def __init__(
        self,
        pipeline_id: PipelineId,
        tenant_id: str,
        name: str,
        launched_by: str,
        sitemaps_urls: Dict,
        description: Optional[str] = None,
        request_headers: Optional[Dict] = None,
        selector_mapping: Optional[Dict] = None,
        excluded_tags: Optional[List] = None,
        excluded_selectors: Optional[List] = None,
        url_address_pattern: Optional[str] = None,
        custom_request_fields: Optional[Dict] = None
    ):
        self._pipeline_id = pipeline_id
        self._tenant_id = tenant_id
        self._launched_by = launched_by
        self._name = name
        self._description = description
        self._completed = False
        self._request_headers = None if not request_headers else request_headers
        self._completed_on = None
        self._selector_mapping = None if not selector_mapping else selector_mapping
        self._excluded_tags = None if not excluded_tags else excluded_tags
        self._excluded_selectors = None if not excluded_selectors else excluded_selectors
        self._sitemaps_urls = sitemaps_urls
        self._url_address_pattern = url_address_pattern
        self._custom_request_fields = None if not custom_request_fields else custom_request_fields

        event = PipelineLaunched(
            self._tenant_id,
            self._pipeline_id.value,
            self._name,
            self._launched_by,
            self._sitemaps_urls,
            self._request_headers,
            self._selector_mapping,
            self._excluded_tags,
            self._excluded_selectors,
            self._description,
            self._custom_request_fields,
            self._url_address_pattern
        )
        self._started_on = event.occurred_on

        self.record_event(event)

    @property
    def id(self) -> PipelineId:
        return self._pipeline_id

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def sitemaps_urls(self) -> Dict:
        return self._sitemaps_urls

    @property
    def url_address_pattern(self) -> Optional[str]:
        return self._url_address_pattern

    @property
    def request_headers(self) -> Optional[Dict]:
        return self._request_headers

    @property
    def selector_mapping(self) -> Optional[Dict]:
        return self._selector_mapping

    @property
    def excluded_tags(self) -> Optional[List]:
        return self._excluded_tags

    @property
    def excluded_selectors(self) -> Optional[List]:
        return self._excluded_selectors

    @property
    def is_completed(self) -> bool:
        return self._completed

    def complete(self) -> None:
        self._completed = True
        self._completed_on = datetime.now()

    def __repr__(self):
        return 'Pipeline <{}>'.format(self._pipeline_id.value)


class PipelineRepository(Repository, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def pipeline_of_tenant_and_id(self, tenant_id: str, pipeline_id: PipelineId):
        raise NotImplementedError

    @staticmethod
    def generate_identifier() -> PipelineId:
        return PipelineId()

    @staticmethod
    def generate_unique_name() -> str:
        return ' '.join(x.capitalize() for x in generate(2))
