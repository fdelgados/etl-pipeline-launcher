from shared.domain.event.event import DomainEvent


class BuildCompleted(DomainEvent):
    EVENT_NAME = "build_completed"

    def __init__(self, tenant_id: str, build_id: str):
        self._tenant_id = tenant_id
        self._build_id = build_id

        super().__init__(self._build_id)

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def build_id(self) -> str:
        return self._build_id
