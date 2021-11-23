from shared.domain.bus.event import DomainEvent


class DuplicityDetected(DomainEvent):
    def __init__(
        self,
        report_id: str,
        address: str,
        another_address: str,
        similarity: float,
    ):
        super().__init__(address)

        self._report_id = report_id
        self._address = address
        self._another_address = another_address
        self._similarity = similarity

    @property
    def report_id(self) -> str:
        return self._report_id

    @property
    def address(self) -> str:
        return self._address

    @property
    def another_address(self) -> str:
        return self._another_address

    @property
    def similarity(self) -> float:
        return self._similarity
