
from shared import Application, Utils, settings
from shared.domain.bus.event import DomainEvent, DomainEventSubscriber, EventStore


class StoreDomainEventOnPublished(DomainEventSubscriber):
    def handle(self, domain_event: DomainEvent) -> None:
        domain_event_class_name = Utils.class_fullname(domain_event)
        context, _ = domain_event_class_name.split(".", maxsplit=1)

        if not settings.is_event_store_enabled_for_context(context):
            return None

        event_store = Application.container().get(
            settings.event_store_id(context)
        )

        if not event_store or not isinstance(event_store, EventStore):
            return None

        event_store.append(domain_event)
