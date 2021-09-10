from typing import List, Dict, Optional
from shared.infrastructure.event import DomainEvent


class EtlStarted(DomainEvent):
    _EVENT_NAME = 'etl_started'

    def __init__(
        self,
        tenant_id: str,
        etl_id: str,
        name: str,
        launched_by: str,
        sitemaps: List,
        custom_request_headers: Optional[Dict],
        selector_mapping: Optional[Dict],
        excluded_tags: Optional[List],
        excluded_selectors: Optional[List],
        description: Optional[str],
        custom_fields: Optional[Dict],
        url_pattern: Optional[str]
    ):
        super().__init__(etl_id)

        self._tenant_id = tenant_id
        self._etl_id = etl_id
        self._name = name
        self._launched_by = launched_by
        self._sitemaps = sitemaps
        self._custom_request_headers = custom_request_headers
        self._selector_mapping = selector_mapping
        self._excluded_tags = excluded_tags
        self._excluded_selectors = excluded_selectors
        self._description = description
        self._custom_fields = custom_fields
        self._url_pattern = url_pattern

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def launched_by(self) -> str:
        return self._launched_by

    @property
    def sitemaps(self) -> List:
        return self._sitemaps

    @property
    def custom_request_header(self) -> Optional[Dict]:
        return self._custom_request_headers

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
    def description(self) -> Optional[str]:
        return self._description

    @property
    def custom_fields(self) -> Optional[Dict]:
        return self._custom_fields

    @property
    def url_pattern(self) -> Optional[str]:
        return self._url_pattern
