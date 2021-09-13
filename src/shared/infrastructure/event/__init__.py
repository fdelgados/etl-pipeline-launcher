import threading
from typing import List
from shared_context.domain.events import DomainEvent
from shared import Application


class DomainEventPublisher:
    @classmethod
    def publish(cls, domain_events: List[DomainEvent]) -> None:
        for domain_event in domain_events:
            cls._publish_event(domain_event)

    @staticmethod
    def _publish_event(domain_event: DomainEvent) -> None:
        domain_event_name = _classname(domain_event)
        event_handlers = Application.container().event_handlers(domain_event_name)

        for subscriber in event_handlers:
            thread = threading.Thread(target=subscriber.handle, args=(domain_event,))
            thread.start()


def _classname(obj):
    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is not None and module != "__builtin__":
        name = f"{module}.{name}"

    return name
