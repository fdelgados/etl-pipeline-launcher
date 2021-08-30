from flask import request, jsonify, make_response
from shared.infrastructure.controller.flask.api import BaseController
from flask_restx import Namespace
from http import HTTPStatus
from datetime import datetime

launcher_api = Namespace(
    'launcher',
    description='ETL pipeline launcher'
)


@launcher_api.route('/')
class Launcher(BaseController):
    def get(self):
        return make_response(
            jsonify(
                status=HTTPStatus.OK,
                datetime=datetime.now(),
                links={
                    "rel": "self",
                    "href": request.url
                }
            ),
            HTTPStatus.OK
        )
