from flask_restx import Resource
from flask import current_app
from shared import ApiBaseError,  settings
from http import HTTPStatus


class BaseController(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

        self._container = current_app.container

    def service(self, service_id: str):
        return self._container.get(service_id)

    @classmethod
    def api_error(cls, error: ApiBaseError, status_code: int):
        error_data = {
            'error': {
                'message': error.message,
                'code': error.code,
                'status': status_code
            }
        }

        headers = {}

        if status_code == HTTPStatus.UNAUTHORIZED:
            headers["WWW-Authenticate"] = f"Bearer realm=\"{settings.api_title()}\", charset=\"UTF-8\""

        return error_data, status_code, headers
