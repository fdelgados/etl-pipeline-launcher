from typing import List

from shared.domain.bus.event import DomainEventSubscriber
from corpus_builder.build.domain.event.urls_retrieved import UrlsRetrieved
from corpus_builder.build.domain.model.build import BuildRepository, BuildId


class UpdateTotalPagesOnUrlsRetrieved(DomainEventSubscriber):
    def __init__(self, build_repository: BuildRepository):
        self._build_repository = build_repository

    def subscribed_to(self) -> List:
        return [UrlsRetrieved.EVENT_NAME]

    def handle(self, domain_event: UrlsRetrieved) -> None:
        build = self._build_repository.build_of_tenant_and_id(
            domain_event.tenant_id, BuildId(domain_event.build_id)
        )

        if not build:
            return

        build.total_pages = domain_event.total_pages

        self._build_repository.save(build)
