from shared.domain.bus.event import DomainEvent


class ReportCreated(DomainEvent):
    def __init__(
        self,
        report_id: str,
        name: str,
        from_corpus: str,
        created_by: str,
        tenant_id: str,
        k_shingle_size: int,
        similarity_threshold: float,
        similarity_threshold_margin: float,
    ):
        super().__init__(report_id)

        self._report_id = report_id
        self._name = name
        self._from_corpus = from_corpus
        self._created_by = created_by
        self._tenant_id = tenant_id
        self._k_shingle_size = k_shingle_size
        self._similarity_threshold = similarity_threshold
        self._similarity_threshold_margin = similarity_threshold_margin

    @property
    def report_id(self) -> str:
        return self._report_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def from_corpus(self) -> str:
        return self._from_corpus

    @property
    def created_by(self) -> str:
        return self._created_by

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def k_shingle_size(self) -> int:
        return self._k_shingle_size

    @property
    def similarity_threshold(self) -> float:
        return self._similarity_threshold

    @property
    def similarity_threshold_margin(self) -> float:
        return self._similarity_threshold_margin
