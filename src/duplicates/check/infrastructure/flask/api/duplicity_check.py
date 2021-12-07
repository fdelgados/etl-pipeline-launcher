from flask import request
from flask_restx import Namespace

from shared.infrastructure.security import authorization_required
from shared.infrastructure.flask.api.basecontroller import BaseController

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

        command = CreateDuplicityCheckCommand(
            params.get("urls"),
            params.get("similarity_threshold"),
            user,
            params.get("corpus"),
        )

        self.dispatch(command)

        return self.response_accepted()
