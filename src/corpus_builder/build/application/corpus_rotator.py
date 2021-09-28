from shared.domain.bus.event import DomainEventSubscriber
from corpus_builder.build.domain.service.corpus_manager import CorpusManager
from corpus_builder.build.domain.event.build_completed import BuildCompleted


class RotateCorpusOnBuildCompleted(DomainEventSubscriber):
    def __init__(self, corpus_manager: CorpusManager):
        super().__init__()

        self._corpus_manager = corpus_manager

    def handle(self, domain_event: BuildCompleted) -> None:
        try:
            self._corpus_manager.rotate(domain_event.corpus_name)
        except ValueError:
            pass
