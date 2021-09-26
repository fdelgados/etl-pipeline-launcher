from shared.domain.bus.event import DomainEventSubscriber
from corpus_builder.build.domain.model.page import PageRepository
from corpus_builder.build.domain.event.build_completed import BuildCompleted


class LinkPagesToCorpusOnBuildCompleted(DomainEventSubscriber):
    def __init__(self, page_repository: PageRepository):
        super().__init__()

        self._page_repository = page_repository

    def handle(self, domain_event: BuildCompleted) -> None:
        try:
            self._page_repository.rename_pages_collection(domain_event.corpus_name)
        except ValueError:
            pass
