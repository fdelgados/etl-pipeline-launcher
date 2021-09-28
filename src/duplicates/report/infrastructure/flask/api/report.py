from http import HTTPStatus
from flask import request, make_response
from flask_restx import Namespace

import shared.infrastructure.environment.global_vars as glob
from shared.infrastructure.security import authorization_required
from shared.infrastructure.flask.api.base_controller import BaseController
from duplicates.report.application.report_creator import ReportCreatorCommand
from duplicates.report.application.identity_generator import NextIdentityQuery

report_api = Namespace("report", description="Near duplicates report generator")


@report_api.route("")
class ReportController(BaseController):
    @authorization_required("create:near-duplicates-report")
    def post(self, user):
        params = request.get_json()

        next_identity_query = self.ask(NextIdentityQuery())
        report_id = next_identity_query.report_id

        command = ReportCreatorCommand(
            report_id,
            params.get("similarity_threshold"),
            params.get("k_shingle_size"),
            user,
        )

        self.dispatch(command)

        response = make_response("", HTTPStatus.ACCEPTED)
        response.headers = {
            "Content-Location": f"{glob.settings.api_url()}/reports/{report_id}"
        }

        return response
