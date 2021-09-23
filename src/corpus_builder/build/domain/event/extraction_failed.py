from shared.domain.event.event import DomainEvent


class ExtractionFailed(DomainEvent):
    def __init__(self, tenant_id: str, build_id: str, address: str):
        self._tenant_id = tenant_id
        self._build_id = build_id
        self._address = address

        super().__init__(build_id)

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def build_id(self) -> str:
        return self._build_id

    @property
    def address(self) -> str:
        return self._address
