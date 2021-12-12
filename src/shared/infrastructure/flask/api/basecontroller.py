import hashlib
import time
import re
from flask import make_response
from typing import Optional, Dict, Union

from http import HTTPStatus
from flask_restx import Resource

from shared.domain.errors.errors import Errors, ApplicationError
from shared.domain.bus.query import Query, QueryBus, Response
from shared.domain.bus.command import Command, CommandBus
from shared.domain.service.logging.logger import Logger
import shared.infrastructure.environment.globalvars as glob


class BaseController(Resource):
    _DEFAULT_STATUS_CODE = HTTPStatus.OK

    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)

        self._query_bus: QueryBus = glob.container.get(
            "shared.domain.bus.query.query_bus"
        )
        self._command_bus: CommandBus = glob.container.get(
            "shared.domain.bus.command.command_bus"
        )
        self._logger: Logger = glob.container.get(
            "shared.domain.service.logging.logger.logger"
        )

    def dispatch(self, command: Command):
        self._command_bus.dispatch(command)

    def ask(self, query: Query) -> Optional[Response]:
        return self._query_bus.ask(query)

    def base_url(self) -> str:
        return glob.settings.api_url()

    @classmethod
    def api_generic_error(cls, error: Exception):
        return cls.api_error(
            ApplicationError(Errors.generic()),
            error,
        )

    @classmethod
    def api_error(
        cls, exception: ApplicationError, from_error: Exception = None
    ):
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        message = exception.error.message
        if exception.error.details:
            message = f"{message}. {exception.error.details}"

        if (
            exception.error == Errors.missing_request_parameter()
            or exception.error == Errors.invalid_request_parameter()
            or exception.error == Errors.limit_exceeded()
        ):
            status_code = HTTPStatus.BAD_REQUEST
        if (
            exception.error == Errors.authorization()
            or exception.error == Errors.missing_access_token()
            or exception.error == Errors.access_token_expired()
        ):
            status_code = HTTPStatus.UNAUTHORIZED

        if exception.error == Errors.entity_not_found():
            status_code = HTTPStatus.NOT_FOUND

        if exception.error == Errors.conflict_error():
            status_code = HTTPStatus.CONFLICT

        error_hash = int(
            hashlib.sha256(
                (str(time.time()) + str(exception.error.code)).encode()
            ).hexdigest()[:8],
            16,
        )
        trace_id = f"ERR-{error_hash}"
        error_data = {
            "error": {
                "message": message,
                "code": exception.error.code,
                "status": status_code,
                "trace_id": trace_id,
            }
        }

        headers = {}

        if status_code == HTTPStatus.UNAUTHORIZED:
            headers[
                "WWW-Authenticate"
            ] = f'Bearer realm="{glob.settings.api_title()}", charset="UTF-8"'

        logger: Logger = glob.container.get(
            "shared.domain.service.logging.logger.logger"
        )

        message = "{} :: {} :: {} {}".format(
            trace_id,
            error_data["error"]["message"],
            type(from_error).__name__ if from_error else "",
            str(from_error) if from_error else "",
        )

        logger.error(message)

        return error_data, status_code, headers

    def _json_response(
        self,
        response: Union[str, Dict],
        status_code: int,
        headers: Optional[Dict] = None,
    ):
        response = make_response(response, status_code)

        response.headers['Content-Type'] = 'application/json'
        if headers:
            for header, value in headers.items():
                response.headers[header] = value

        return response

    def response_ok(self, response: Dict, headers: Optional[Dict] = None):
        return self._json_response(response, HTTPStatus.OK, headers)

    def response_accepted(
        self,
        response: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ):
        return self._json_response(
            response if response is not None else "",
            HTTPStatus.ACCEPTED,
            headers,
        )

    def _camelize_keys(self, dict_obj: Dict):
        assert type(dict_obj) == dict

        converted_dict_obj = {}
        for snake_case_k in dict_obj:
            camel_case_k = re.sub(
                "_([a-z])", lambda match: match.group(1).upper(), snake_case_k
            )
            value = dict_obj[snake_case_k]

            if type(value) == dict:
                converted_dict_obj[camel_case_k] = self._camelize_keys(value)
            elif type(value) == list:
                converted_list_items = []
                for item in value:
                    converted_list_items.append(self._camelize_keys(item))
                converted_dict_obj[camel_case_k] = converted_list_items
            else:
                converted_dict_obj[camel_case_k] = dict_obj[snake_case_k]

        return converted_dict_obj
