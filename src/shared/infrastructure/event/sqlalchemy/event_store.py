from shared_context.infrastructure.persistence.sqlalchemy import DbalService

from shared import settings

from shared.infrastructure.event import DomainEvent
from shared.domain.service.event.event_store import EventStore


class SqlAlchemyEventStore(EventStore, DbalService):
    def __init__(self) -> None:
        super().__init__(settings.database_dsn('corpus'))

    def store(self, event: DomainEvent):
        sentence = '''
            INSERT INTO event_store (etl_id, occurred_on, event_data, event_name, aggregate_id)
            VALUES (:etl_id, :occurred_on, :event_data, :event_name, :aggregate_id)
        '''

        self.execute(
            sentence,
            etl_id=event.etl_id,
            occurred_on=event.occurred_on,
            event_data=event.serialize(),
            event_name=event.event_name(),
            aggregate_id=event.aggregate_id
        )

