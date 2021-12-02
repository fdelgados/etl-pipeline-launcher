from typing import List, Dict
from sqlalchemy import desc, asc

from shared.domain.model.aggregate import AggregateRoot
from shared.domain.model.repository import Repository as BaseRepository

from shared.infrastructure.persistence.sqlalchemy.session import (
    session_scope,
    SessionFactory,
)


class Repository(BaseRepository):
    def __init__(self, aggregate: AggregateRoot, dsn: str):
        self._aggregate = aggregate
        self._dsn = dsn
        self._session = SessionFactory.create(self._dsn)

    def add(self, aggregate: AggregateRoot) -> None:
        with session_scope(self._dsn) as session:
            session.add(aggregate)
            # session.commit()

    def save(self, aggregate: AggregateRoot) -> None:
        with session_scope(self._dsn) as session:
            session.add(aggregate)
            # session.commit()

    def find(self, **kwargs) -> AggregateRoot:
        session = self._session()

        return session.query(self._aggregate).filter_by(**kwargs).first()
        # with session_scope(self._dsn) as session:
        #     result = session.query(self._aggregate).filter_by(**kwargs).first()
        #
        # return result

    def find_all(self, order_by: Dict = None, **kwargs) -> List[AggregateRoot]:
        # with session_scope(self._dsn) as session:
        session = self._session()
        query = session.query(self._aggregate).filter_by(**kwargs)
        if order_by:
            for field, direction in order_by.items():
                if direction == "desc":
                    order_expression = desc(
                        self._aggregate.__dict__[field]
                    )
                else:
                    order_expression = asc(self._aggregate.__dict__[field])

                query = query.order_by(order_expression)

        results = query.all()

        return results
