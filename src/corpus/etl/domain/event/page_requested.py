from datetime import datetime

from shared_context.domain.events import DomainEvent


class PageRequested(DomainEvent):
    _EVENT_NAME = "page_requested"

    def __init__(
        self,
        etl_id: str,
        address: str,
        status_code: int,
        status: str,
        modified_on: datetime,
    ):
        self._etl_id = etl_id
        self._address = address
        self._status_code = status_code
        self._status = status
        self._modified_on = modified_on

        super().__init__(address)

    def event_name(self) -> str:
        return self._EVENT_NAME

    @property
    def etl_id(self) -> str:
        return self._etl_id

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
