from flask import request
from flask_restx import Namespace

import shared.infrastructure.environment.globalvars as g_vars
from shared.infrastructure.security import authorization_required
from shared.infrastructure.flask.api.basecontroller import BaseController
from duplicates.check.application.duplicitycheckcreator import (
    GenerateNextIdentityQuery,
)
from duplicates.check.application.results_service import (
    RetrieveDuplicityCheckResultsQuery,
)
from duplicates.check.application.duplicitycheckcreator import (
    CreateDuplicityCheckCommand,
)


duplicity_check_api = Namespace(
    "duplicates", description="Search duplicates for a specific content"
)


@duplicity_check_api.route("")
class DuplicityCheckController(BaseController):
    @authorization_required("check:duplicity")
    def post(self, user):
        params = request.get_json()
        check_id = self._check_id()

        command = CreateDuplicityCheckCommand(
            check_id,
            params.get("urls"),
            params.get("similarity_threshold"),
            user,
            params.get("corpus"),
        )

        self.dispatch(command)

        results_url = "{}/duplicity-checks/{}/results".format(
            g_vars.settings.api_url(),
            check_id,
        )

        return self.response_accepted(
            {
                "check_id": check_id,
                "check_results_url": results_url,
            },
            {
                "Content-Location": results_url,
            },
        )

    def _check_id(self) -> str:
        query = GenerateNextIdentityQuery()
        response = self.ask(query)

        return response.value()


@duplicity_check_api.route("/results")
class GetCheckedUrlsSinceDateController(BaseController):
    @authorization_required("check:duplicity")
    def get(self, user):
        params = request.args

        query = RetrieveDuplicityCheckResultsQuery(
            str(params.get("since")),
        )

        response = self.ask(query)

        return self.response_ok(
            {
                "data": response.value().serialize()
            }
        )


@duplicity_check_api.route("/<string:check_id>/results")
class GetCheckedUrlsOfCheckController(BaseController):
    @authorization_required("check:duplicity")
    def get(self, user, check_id: str):
        query = RetrieveDuplicityCheckResultsQuery(check_id=check_id)

        response = self.ask(query)

        return self.response_ok(
            {
                "data": response.value().serialize()
            }
        )
