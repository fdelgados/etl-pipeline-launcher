from shared_context.domain.events import DomainEvent


class ReportCreated(DomainEvent):
    _EVENT_NAME = 'report_created'

    def __init__(
        self,
        report_id: str,
        name: str,
        created_by: str,
        k_shingle_size: int,
        similarity_threshold: float
    ):
        super().__init__()

        self._report_id = report_id
        self._name = name
        self._created_by = created_by
        self._k_shingle_size = k_shingle_size
        self._similarity_threshold = similarity_threshold

    @property
    def report_id(self) -> str:
        return self._report_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def created_by(self) -> str:
        return self._created_by

    @property
    def k_shingle_size(self) -> int:
        return self._k_shingle_size

    @property
    def similarity_threshold(self) -> float:
        return self._similarity_threshold

    def event_name(self) -> str:
        return self._EVENT_NAME
