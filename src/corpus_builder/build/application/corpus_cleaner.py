from shared.domain.bus.event import DomainEventSubscriber
from corpus_builder.build.domain.service.corpus_manager import CorpusManager
from corpus_builder.build.domain.event.build_aborted import BuildAborted


class CleanCorpusOnBuildAborted(DomainEventSubscriber):
    def __init__(self, corpus_manager: CorpusManager):
        super().__init__()

        self._corpus_manager = corpus_manager

    def handle(self, domain_event: BuildAborted) -> None:
        try:
            self._corpus_manager.clean(domain_event.corpus_name)
        except ValueError:
            pass
