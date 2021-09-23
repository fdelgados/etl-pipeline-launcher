from http import HTTPStatus
from flask import request
from flask_restx import Namespace

from shared import settings, InvalidRequestParamsException
from shared.infrastructure.security import (
    authorization_required,
    AuthorizationError,
    ExpiredTokenException,
)
from shared.infrastructure.flask.api.base_controller import BaseController
from duplicates.report.application.create.report_creator import ReportCreatorCommand

report_api = Namespace("report", description="Near duplicates report generator")


@report_api.errorhandler(AuthorizationError)
@report_api.errorhandler(ExpiredTokenException)
def handle_authorization_error(error):
    return BaseController.api_error(error, HTTPStatus.UNAUTHORIZED)


@report_api.errorhandler(InvalidRequestParamsException)
def handle_value_error(error):
    return BaseController.api_error(error, HTTPStatus.BAD_REQUEST)


@report_api.route("")
class ReportController(BaseController):
    @authorization_required("create:near-duplicates-report")
    def post(self, user):
        params = request.get_json()

        command = ReportCreatorCommand(
            params.get("similarity_threshold"), params.get("k_shingle_size"), user
        )

        self.dispatch(command)

        return self.response(
            HTTPStatus.ACCEPTED, {"Location": f"{settings.api_url()}/reports/report_id"}
        )
