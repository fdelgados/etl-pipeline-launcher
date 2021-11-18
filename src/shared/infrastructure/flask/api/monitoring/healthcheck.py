from datetime import datetime
from http import HTTPStatus
from flask import make_response
from flask_restx import Namespace

import shared.infrastructure.environment.globalvars as glob

from shared.infrastructure.flask.api.basecontroller import BaseController


health_check = Namespace("health_check", description="Health check endpoint")


@health_check.route("/health-check")
class BuildListController(BaseController):
    def get(self):
        health_info = {
            "status": "OK",
            "version": glob.settings.api_version(),
            "date": datetime.now(),
        }

        return make_response(
            self.json_response(**health_info),
            HTTPStatus.OK,
        )
