from shared.infrastructure.event import DomainEvent


class ExtractionStarted(DomainEvent):
    _EVENT_NAME = "extraction_started"
