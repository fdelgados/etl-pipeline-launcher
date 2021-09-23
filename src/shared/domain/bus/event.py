import abc
from typing import List

from shared.domain.event.event import DomainEvent


class DomainEventSubscriber(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def subscribed_to(self) -> List:
        raise NotImplementedError

    @abc.abstractmethod
    def handle(self, domain_event: DomainEvent) -> None:
        raise NotImplementedError


class EventBus(metaclass=abc.ABCMeta):
    def publish(self, *domain_events: DomainEvent) -> None:
        for domain_event in domain_events:
            self._do_publish(domain_event)

    @abc.abstractmethod
    def _do_publish(self, domain_event: DomainEvent) -> None:
        raise NotImplementedError
