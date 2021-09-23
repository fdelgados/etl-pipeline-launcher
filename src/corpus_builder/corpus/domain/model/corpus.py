import abc
from typing import Optional, List, Dict

from shared.domain.model.repository import Repository
from shared.domain.model.aggregate import AggregateRoot


class Corpus(AggregateRoot):
    def __init__(self, tenant_id: str, name: str):
        self._tenant_id = tenant_id
        self._name = name
        self._sitemaps = None
        self._description = None
        self._request_headers = None
        self._selector_mapping = None
        self._excluded_tags = None
        self._excluded_selectors = None
        self._url_address_pattern = None
        self._custom_request_fields = None

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def sitemaps(self) -> List:
        return self._sitemaps

    @sitemaps.setter
    def sitemaps(self, sitemaps: List):
        self._sitemaps = sitemaps

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._description = description

    @property
    def request_headers(self) -> Optional[Dict]:
        return self._request_headers

    @request_headers.setter
    def request_headers(self, request_headers: Dict) -> None:
        self._request_headers = request_headers

    @property
    def selector_mapping(self) -> Optional[Dict]:
        return self._selector_mapping

    @selector_mapping.setter
    def selector_mapping(self, selector_mapping: Dict) -> None:
        self._selector_mapping = selector_mapping

    @property
    def excluded_tags(self) -> Optional[List]:
        return self._excluded_tags

    @excluded_tags.setter
    def excluded_tags(self, excluded_tags: List) -> None:
        self._excluded_tags = excluded_tags

    @property
    def excluded_selectors(self) -> Optional[List]:
        return self._excluded_selectors

    @excluded_selectors.setter
    def excluded_selectors(self, excluded_selectors: List) -> None:
        self._excluded_selectors = excluded_selectors

    @property
    def url_address_pattern(self) -> Optional[str]:
        return self._url_address_pattern

    @url_address_pattern.setter
    def url_address_pattern(self, url_address_pattern) -> None:
        self._url_address_pattern = url_address_pattern

    @property
    def custom_request_fields(self) -> Optional[Dict]:
        return self._custom_request_fields

    @custom_request_fields.setter
    def custom_request_fields(self, custom_request_fields: Dict) -> None:
        self._custom_request_fields = custom_request_fields


class CorpusRepository(Repository, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def corpus_of_tenant_and_name(self, tenant_id: str, name: str) -> Optional[Corpus]:
        raise NotImplementedError

    @abc.abstractmethod
    def corpora_of_tenant(self, tenant_id: str) -> List[Corpus]:
        raise NotImplementedError
