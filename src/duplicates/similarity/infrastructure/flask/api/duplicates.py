from http import HTTPStatus
from flask import request, make_response
from flask_restx import Namespace

import shared.infrastructure.environment.globalvars as glob
from shared.infrastructure.security import authorization_required
from shared.infrastructure.flask.api.basecontroller import BaseController


duplicates_api = Namespace(
    "duplicates", description="Search duplicates for a specific content"
)


@duplicates_api.route("")
class DuplicationCheckController(BaseController):
    @authorization_required("get:content-duplicates")
    def post(self, user):
        pass
