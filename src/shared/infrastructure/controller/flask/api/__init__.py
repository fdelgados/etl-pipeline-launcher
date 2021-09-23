from typing import Optional, Dict

from http import HTTPStatus
from flask import make_response
from flask_restx import Resource

from shared import Application
from shared import ApiBaseError, ErrorCodes, settings
from shared.domain.bus.query import Query, QueryBus, Response
from shared.domain.bus.command import Command, CommandBus


class BaseController(Resource):
    _DEFAULT_STATUS_CODE = HTTPStatus.OK

    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)

        self._container = Application.container()
        self._query_bus: QueryBus = self._container.get(
            "shared.domain.bus.query.query_bus"
        )
        self._command_bus: CommandBus = self._container.get(
            "shared.domain.bus.command.command_bus"
        )

    def service(self, service_id: str):
        return self._container.get(service_id)

    def dispatch(self, command: Command):
        self._command_bus.dispatch(command)

    def ask(self, query: Query) -> Optional[Response]:
        return self._query_bus.ask(query)

    @classmethod
    def api_generic_error(cls, error: Exception):
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        error_data = {
            "error": {
                "message": str(error),
                "code": ErrorCodes.GENERIC_ERROR,
                "status": status_code,
            }
        }

        return error_data, status_code

    @classmethod
    def api_error(cls, error: ApiBaseError, status_code: int):
        error_data = {
            "error": {
                "message": error.message,
                "code": error.code,
                "status": status_code,
            }
        }

        headers = {}

        if status_code == HTTPStatus.UNAUTHORIZED:
            headers[
                "WWW-Authenticate"
            ] = f'Bearer realm="{settings.api_title()}", charset="UTF-8"'

        return error_data, status_code, headers

    def response(
        self,
        status_code: Optional[int] = None,
        headers: Optional[Dict] = None,
        **kwargs,
    ):
        payload = ""
        if kwargs:
            payload = kwargs

        if not status_code:
            status_code = self._DEFAULT_STATUS_CODE

        response = make_response(payload, status_code)
        if headers:
            response.headers = headers

        return response


def _classname(obj):
    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is not None and module != "__builtin__":
        name = f"{module}.{name}"

    return name
