from __future__ import annotations

import abc

from typing import Any
from dataclasses import dataclass


class QueryError(RuntimeError):
    pass


class QueryNotRegisteredError(QueryError):
    def __init__(self, query: Query) -> None:
        query_class = type(query).__name__

        super().__init__(
            f"The query <{query_class}> hasn't a query handler associated"
        )


class QueryNotCallableError(QueryError):
    def __init__(self, query: Query) -> None:
        query_class = type(query).__name__

        super().__init__(f"The query <{query_class}> is not callable")


@dataclass(frozen=True)
class Query(metaclass=abc.ABCMeta):
    pass


class Response(metaclass=abc.ABCMeta):
    def value(self) -> Any:
        raise NotImplementedError


class QueryHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, query: Query) -> Response:
        raise NotImplementedError


class QueryBus(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def ask(self, query: Query) -> Response:
        raise NotImplementedError
