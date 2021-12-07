import abc


class Corpus:
    def __init__(
        self,
        name: str,
        request_headers: dict,
        excluded_tags: list,
        excluded_selectors: list,
        selector_mapping: dict,
    ):
        self._name = name
        self._request_headers = request_headers
        self._excluded_tags = excluded_tags
        self._excluded_selectors = excluded_selectors
        self._selector_mapping = selector_mapping

    @property
    def name(self) -> str:
        return self._name

    @property
    def request_headers(self) -> dict:
        return self._request_headers

    @property
    def excluded_tags(self) -> list:
        return self._excluded_tags

    @property
    def excluded_selectors(self) -> list:
        return self._excluded_selectors

    @property
    def selector_mapping(self) -> dict:
        return self._selector_mapping


class CorpusRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def corpus_of_name(self, tenant_id: str, name: str) -> Corpus:
        raise NotImplementedError
