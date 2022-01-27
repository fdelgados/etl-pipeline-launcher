from shared.domain.bus.event import DomainEvent


class DuplicityCheckCompleted(DomainEvent):
    def __init__(self, check_id: str):
        super().__init__(check_id)

        self._check_id = check_id

    @property
    def check_id(self) -> str:
        return self._check_id
