from shared.domain.bus.event import DomainEvent


class DuplicityDetected(DomainEvent):
    def __init__(
        self,
        report_id: str,
        address: str,
        another_address: str,
        similarity: float,
        is_in_allowed_margin: bool
    ):
        super().__init__(address)

        self._report_id = report_id
        self._address = address
        self._another_address = another_address
        self._similarity = similarity
        self._is_in_allowed_margin = is_in_allowed_margin

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

    @property
    def is_in_allowed_margin(self) -> bool:
        return self._is_in_allowed_margin
