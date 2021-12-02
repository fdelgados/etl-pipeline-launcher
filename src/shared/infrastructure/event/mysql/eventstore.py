from typing import List

from shared.domain.bus.event import EventStore
from shared.domain.event.storedevent import StoredEvent
from shared.infrastructure.persistence.sqlalchemy.dbal import DbalService


class MysqlEventStore(EventStore):
    def __init__(self, db_service: DbalService):
        self._db_service = db_service

    def append(self, stored_event: StoredEvent) -> None:
        sentence = """
            INSERT INTO event_store (
                id,
                occurred_on,
                event_data,
                event_name,
                aggregate_id
            )
            VALUES (:id, :occurred_on, :event_data, :event_name, :aggregate_id)
        """

        self._db_service.execute(
            sentence,
            id=stored_event.event_id,
            occurred_on=stored_event.occurred_on,
            event_data=stored_event.event_data,
            event_name=stored_event.event_name,
            aggregate_id=stored_event.aggregate_id,
        )

    def events_since(self, domain_event_id: int) -> List[StoredEvent]:
        pass

    def events_by_type(self, type_name: str, **kwargs) -> List[StoredEvent]:
        sentence = """
            SELECT id, occurred_on, event_data, event_name, aggregate_id
            FROM event_store
            WHERE event_name IN :type_names
        """

        self._db_service.execute(sentence)
