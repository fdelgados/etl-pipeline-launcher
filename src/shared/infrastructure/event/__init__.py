import threading
import abc
from typing import List, Optional, Any
from shared_context.domain.events import DomainEvent as BaseDomainEvent
from shared import Application


__all__ = ['DomainEvent', 'DomainEventPublisher']


class DomainEvent(BaseDomainEvent, metaclass=abc.ABCMeta):
    def __init__(self, pipeline_id: str, aggregate_id: Optional[Any] = None):
        self._pipeline_id = pipeline_id

        if not aggregate_id:
            aggregate_id = self._pipeline_id

        super().__init__(aggregate_id)

    @property
    def pipeline_id(self):
        return self._pipeline_id


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
            # subscriber.handle(domain_event)
            thread = threading.Thread(target=subscriber.handle, args=(domain_event, ))
            thread.start()


def _classname(obj):
    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is not None and module != '__builtin__':
        name = f'{module}.{name}'

    return name
