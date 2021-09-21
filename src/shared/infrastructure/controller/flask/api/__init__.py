from typing import Optional, Dict

from http import HTTPStatus
from flask import make_response
from flask_restx import Resource
from shared import Application
from shared import ApiBaseError, ErrorCodes, settings


class BaseController(Resource):
    _DEFAULT_STATUS_CODE = HTTPStatus.OK

    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)

        self._container = Application.container()

    def service(self, service_id: str):
        return self._container.get(service_id)

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
        **kwargs
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
