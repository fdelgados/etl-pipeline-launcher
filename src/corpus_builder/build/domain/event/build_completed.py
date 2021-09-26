from shared.domain.bus.event import DomainEvent


class BuildCompleted(DomainEvent):
    def __init__(self, tenant_id: str, build_id: str, corpus_name: str):
        self._tenant_id = tenant_id
        self._build_id = build_id
        self._corpus_name = corpus_name

        super().__init__(self._build_id)

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def build_id(self) -> str:
        return self._build_id

    @property
    def corpus_name(self) -> str:
        return self._corpus_name
