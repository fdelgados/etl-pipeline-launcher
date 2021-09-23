import abc
from functools import wraps

from typing import List

from shared import Application, Utils
from shared.domain.event.event import DomainEvent


class EventStore(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def append(self, domain_event: DomainEvent) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def events_since(self, domain_event_id: int) -> List[DomainEvent]:
        raise NotImplementedError

    @abc.abstractmethod
    def events_by_type(self, *type_name: str, **kwargs) -> List[DomainEvent]:
        raise NotImplementedError


def store_event(arg=None):
    def decorator(func):
        @wraps(func)
        def decorated_function(self, domain_event: DomainEvent):
            if not domain_event or not isinstance(domain_event, DomainEvent):
                return func(self, domain_event)

            caller_class_name = Utils.class_fullname(domain_event)
            context, _ = caller_class_name.split(".", maxsplit=1)

            event_store = Application.container().get(
                f"{context}.domain.event.event_store.event_store"
            )

            if not event_store or not isinstance(event_store, EventStore):
                return func(self, domain_event)

            event_store.append(domain_event)

            return func(self, domain_event)

        return decorated_function

    if callable(arg):
        return decorator(arg)

    return decorator
