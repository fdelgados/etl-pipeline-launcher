from dataclasses import dataclass, field
from typing import List
from shared_context import Command, CommandHandler
from shared_context.application import Response

from corpus_builder.corpus.domain.model.corpus import CorpusRepository, Corpus


@dataclass(frozen=True)
class CorpusCreatorCommand(Command):
    tenant_id: str
    name: str
    sitemaps: list
    custom_request_headers: dict = field(default_factory={})
    selector_mapping: dict = field(default_factory={})
    excluded_tags: List[str] = field(default_factory=[])
    excluded_selectors: List[str] = field(default_factory=[])
    description: str = field(default=None)
    custom_fields: dict = field(default_factory={})
    url_address_pattern: str = None


@dataclass(frozen=True)
class CorpusCreatorResponse(Response):
    updated: bool


class CorpusCreator(CommandHandler):
    def __init__(self, corpus_repository: CorpusRepository):
        self._corpus_repository = corpus_repository

    def handle(self, command: CorpusCreatorCommand) -> CorpusCreatorResponse:
        is_update = True
        corpus = self._corpus_repository.config_of_tenant_and_name(
            command.tenant_id,
            command.name
        )

        if not corpus:
            is_update = True
            corpus = Corpus(command.tenant_id, command.name)

        corpus.sitemaps = command.sitemaps

        if command.description:
            corpus.description = command.description

        if command.custom_request_headers:
            corpus.request_headers = command.custom_request_headers

        if command.selector_mapping:
            corpus.selector_mapping = command.selector_mapping

        if command.excluded_tags:
            corpus.excluded_tags = command.excluded_tags

        if command.excluded_selectors:
            corpus.excluded_selectors = command.excluded_selectors

        if command.url_address_pattern:
            corpus.url_address_pattern = command.url_address_pattern

        if command.custom_fields:
            corpus.custom_request_fields = command.custom_fields

        self._corpus_repository.save(corpus)

        return CorpusCreatorResponse(updated=is_update)

    def _retrieve_corpus(self, tenant_id: str, name: str) -> Corpus:
        corpus = self._corpus_repository.config_of_tenant_and_name(
            tenant_id,
            name
        )

        if not corpus:
            return Corpus(tenant_id, name)
