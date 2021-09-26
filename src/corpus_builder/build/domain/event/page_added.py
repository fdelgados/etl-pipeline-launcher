from datetime import datetime

from shared.domain.bus.event import DomainEvent


class PageAdded(DomainEvent):
    def __init__(
        self,
        tenant_id: str,
        build_id: str,
        address: str,
        status_code: int,
        status: str,
        modified_on: datetime,
        corpus_name: str,
    ):
        self._tenant_id = tenant_id
        self._build_id = build_id
        self._address = address
        self._status_code = status_code
        self._status = status
        self._modified_on = modified_on
        self._corpus_name = corpus_name

        super().__init__(address)

    @property
    def build_id(self) -> str:
        return self._build_id

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

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

    @property
    def corpus_name(self):
        return self._corpus_name
