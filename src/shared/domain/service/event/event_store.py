import abc

from shared_context.domain.events import DomainEvent


class EventStore(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def store(self, event: DomainEvent):
        raise NotImplementedError
