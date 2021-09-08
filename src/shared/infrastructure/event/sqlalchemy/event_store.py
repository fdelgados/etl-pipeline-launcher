from sqlalchemy import create_engine, exc, text

from typing import Dict

from shared.infrastructure.event import DomainEvent

from shared.domain.service.event.event_store import EventStore


class ConnectionBuilder:
    _connection = None

    @classmethod
    def build(cls, connection_data: Dict):
        if not cls._connection:
            dsn = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
                connection_data.get('user'),
                connection_data.get('password'),
                connection_data.get('host'),
                connection_data.get('name')
            )

            cls._connection = create_engine(dsn)

        return cls._connection


class SqlAlchemyEventStore(EventStore):
    def __init__(self, host: str, user: str, password: str, db_name: str):
        self._connection_data = {
            'host': host,
            'user': user,
            'password': password,
            'name': db_name
        }

    def store(self, event: DomainEvent):
        connection = ConnectionBuilder.build(self._connection_data)

        sentence = '''
            INSERT INTO event_store (pipeline_id, occurred_on, event_data, event_name, aggregate_id)
            VALUES (:pipeline_id, :occurred_on, :event_data, :event_name, :aggregate_id)
        '''

        with connection.connect() as conn:
            try:
                conn.execute(
                    text(sentence),
                    pipeline_id=event.pipeline_id,
                    occurred_on=event.occurred_on,
                    event_data=event.serialize(),
                    event_name=event.event_name(),
                    aggregate_id=event.aggregate_id
                )
            except (exc.DBAPIError, exc.IntegrityError):
                raise
            finally:
                conn.close()
