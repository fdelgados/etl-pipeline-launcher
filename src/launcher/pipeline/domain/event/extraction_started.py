from shared.infrastructure.event import DomainEvent


class ExtractionStarted(DomainEvent):
    def event_name(self) -> str:
        return 'extraction_started'
