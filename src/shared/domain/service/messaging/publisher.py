import abc
from shared_context.domain.events import DomainEvent


class EventPublisher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def publish(self, event: DomainEvent, publisher: str) -> None:
        raise NotImplementedError
