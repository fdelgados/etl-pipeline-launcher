from typing import Optional
from shared import Utils, Application
from shared.domain.bus.query import (
    Query,
    QueryHandler,
    QueryBus,
    Response,
    QueryNotRegisteredError,
    QueryNotCallableError,
)


class QueryBusImpl(QueryBus):
    def ask(self, query: Query) -> Optional[Response]:
        container = Application.container()

        query_fullname = Utils.class_fullname(query)
        module, query_name = query_fullname.rsplit(".", maxsplit=1)

        handler_id = "{}.{}_handler".format(
            module, Utils.camel_case_to_snake(query_name)
        )

        query_handler: QueryHandler = container.get(handler_id)

        if not query_handler:
            raise QueryNotRegisteredError(query)

        if not isinstance(query_handler, QueryHandler):
            raise QueryNotRegisteredError(query)

        if not hasattr(query_handler, "handle") or not callable(query_handler.handle):
            raise QueryNotCallableError(query)

        return query_handler.handle(query)
