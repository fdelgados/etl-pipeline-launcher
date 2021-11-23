from http import HTTPStatus
from flask import request, make_response
from flask_restx import Namespace

import shared.infrastructure.environment.globalvars as glob
from shared.infrastructure.security import authorization_required
from shared.infrastructure.flask.api.basecontroller import BaseController
from duplicates.report.application.reportservice import (
    ReportCreatorCommand,
    NextIdentityQuery,
)

report_api = Namespace(
    "report", description="Near duplicates report generator"
)


@report_api.route("")
class ReportController(BaseController):
    @authorization_required("create:near-duplicates-report")
    def post(self, user):
        params = request.get_json()

        next_identity_response = self.ask(NextIdentityQuery())
        report_id = next_identity_response.value()

        command = ReportCreatorCommand(
            report_id,
            params.get("corpus"),
            params.get("similarity_threshold"),
            params.get("k_shingle_size"),
            user,
        )

        self.dispatch(command)

        response = make_response("", HTTPStatus.ACCEPTED)
        response.headers = {
            "Content-Location": "{}/reports/{}".format(
                glob.settings.api_url(),
                report_id,
            )
        }

        return response
