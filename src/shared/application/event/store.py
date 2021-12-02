from shared.utils import class_fullname
from shared.domain.model.valueobject.uid import Uuid
from shared.domain.bus.event import (
    DomainEvent,
    DomainEventSubscriber,
    EventStore,
)
from shared.domain.event.storedevent import StoredEvent
import shared.infrastructure.environment.globalvars as glob


class StoreDomainEventOnPublished(DomainEventSubscriber):
    def handle(self, domain_event: DomainEvent) -> None:
        domain_event_class_name = class_fullname(domain_event)
        context, _ = domain_event_class_name.split(".", maxsplit=1)

        if not glob.settings.is_event_store_enabled_for_context(context):
            return None

        event_store = glob.container.get(glob.settings.event_store_id(context))

        if not event_store or not isinstance(event_store, EventStore):
            return None

        stored_event = StoredEvent(
            str(Uuid()),
            domain_event.aggregate_id,
            domain_event.occurred_on,
            domain_event.serialize(),
            domain_event.type_name(),
        )

        event_store.append(stored_event)

        return None
