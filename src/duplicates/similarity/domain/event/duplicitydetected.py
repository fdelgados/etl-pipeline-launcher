from shared.domain.bus.event import DomainEvent


class DuplicityDetected(DomainEvent):
    def __init__(self):
        super().__init__()
