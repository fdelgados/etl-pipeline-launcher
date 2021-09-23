from shared.domain.event.event import DomainEvent


class BuildStarted(DomainEvent):
    def __init__(
        self,
        tenant_id: str,
        build_id: str,
        name: str,
        started_by: str,
        corpus_name: str,
    ):
        super().__init__(build_id)

        self._tenant_id = tenant_id
        self._build_id = build_id
        self._name = name
        self._started_by = started_by
        self._corpus_name = corpus_name

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def build_id(self) -> str:
        return self._build_id

    @property
    def started_by(self) -> str:
        return self._started_by

    @property
    def corpus_name(self) -> str:
        return self._corpus_name
