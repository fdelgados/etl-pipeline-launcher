from flask import request, jsonify, Blueprint
from http import HTTPStatus
from datetime import datetime

launcher_api = Blueprint("launcher_api", __name__)


@launcher_api.route("/", methods=["GET"])
def health_check():
    return jsonify(
        status=HTTPStatus.OK,
        datetime=datetime.now(),
        links={
            "rel": "self",
            "href": request.url}
    ), HTTPStatus.OK
