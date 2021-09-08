from datetime import datetime

from shared.infrastructure.event import DomainEvent


class PageRequested(DomainEvent):
    def __init__(
        self,
        pipeline_id: str,
        address: str,
        status_code: int,
        status: str,
        modified_on: datetime
    ):

        self._pipeline_id = pipeline_id
        self._address = address
        self._status_code = status_code
        self._status = status
        self._modified_on = modified_on

        super().__init__(pipeline_id, address)

    @property
    def address(self) -> str:
        return self._address

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def status(self) -> str:
        return self._status

    @property
    def modified_on(self) -> datetime:
        return self._modified_on

    def event_name(self) -> str:
        return 'page_requested'
