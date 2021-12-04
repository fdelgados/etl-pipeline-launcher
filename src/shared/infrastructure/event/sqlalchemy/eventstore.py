from typing import List

from sqlalchemy import Table, String, Column, DateTime, Text

from sqlalchemy.orm import registry

from shared.domain.bus.event import EventStore
from shared.domain.event.storedevent import StoredEvent

import shared.infrastructure.environment.globalvars as global_vars

from shared.infrastructure.persistence.sqlalchemy.session import session_scope


def _map_stored_event():
    mapper_registry = registry()

    events_table = Table(
        "event_store",
        mapper_registry.metadata,
        Column("id", String(36), nullable=False, primary_key=True),
        Column("aggregate_id", String(255), nullable=False),
        Column("event_name", String(200), nullable=False),
        Column("event_data", Text, nullable=False),
        Column("occurred_on", DateTime, nullable=True),
        extend_existing=True,
    )

    mapper_registry.map_imperatively(
        StoredEvent,
        events_table,
        column_prefix="_",
        properties={"_event_id": events_table.c.id},
    )


class SqlAlchemyEventStore(EventStore):
    def __init__(self, context: str):
        _map_stored_event()

        self._dsn = global_vars.settings.database_dsn(context)

    def append(self, stored_event: StoredEvent) -> None:
        with session_scope(self._dsn) as session:
            session.add(stored_event)

    def events_since(self, domain_event_id: int) -> List[StoredEvent]:
        pass

    def events_by_type(self, type_name: str, **kwargs) -> List[StoredEvent]:
        pass
