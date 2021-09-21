from shared_context.domain.events import DomainEvent


class ExtractionFailed(DomainEvent):
    _EVENT_NAME = "extraction_failed"

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

    def event_name(self) -> str:
        return self._EVENT_NAME
