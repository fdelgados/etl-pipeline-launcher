from shared.domain.bus.event import DomainEvent


class PageAnalyzed(DomainEvent):
    def __init__(self, report_id: str, address: str):
        super().__init__(address)

        self._report_id = report_id
        self._address = address

    @property
    def report_id(self) -> str:
        return self._report_id

    @property
    def address(self) -> str:
        return self._address
