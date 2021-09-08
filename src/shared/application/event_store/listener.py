from shared_context.domain.events import DomainEvent
from shared.domain.service.event.event_store import EventStore


class StoreEventOnPublish:
    def __init__(self, event_store: EventStore):
        self._event_store = event_store

    def handle(self, event: DomainEvent):
        self._event_store.store(event)
