from dataclasses import dataclass, field
from typing import List
from shared.domain.bus.command import Command, CommandHandler

from corpus_builder.build.domain.model.corpus import CorpusRepository, Corpus


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


class CorpusCreatorCommandHandler(CommandHandler):
    def __init__(self, corpus_repository: CorpusRepository):
        self._corpus_repository = corpus_repository

    def handle(self, command: CorpusCreatorCommand) -> None:
        corpus = self._corpus_repository.corpus_of_tenant_and_name(
            command.tenant_id, command.name
        )

        if not corpus:
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
