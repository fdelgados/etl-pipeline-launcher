from shared.domain.event.event import DomainEvent
from shared.domain.event.event_store import EventStore
from shared.infrastructure.persistence.sqlalchemy.dbal import DbalService


class MysqlEventStore(EventStore):
    def __init__(self, db_service: DbalService):
        self._db_service = db_service

    def append(self, domain_event: DomainEvent) -> None:
        sentence = """
            INSERT INTO event_store (occurred_on, event_data, event_name, aggregate_id)
            VALUES (:occurred_on, :event_data, :event_name, :aggregate_id)
        """

        self._db_service.execute(
            sentence,
            occurred_on=domain_event.occurred_on,
            event_data=domain_event.serialize(),
            event_name=type(domain_event).__name__,
            aggregate_id=domain_event.aggregate_id,
        )
