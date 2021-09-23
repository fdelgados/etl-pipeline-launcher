from http import HTTPStatus
from flask_restx import Namespace

from shared import InvalidRequestParamsException
from shared.infrastructure.security import (
    authorization_required,
    AuthorizationError,
    ExpiredTokenException,
)
from shared.infrastructure.flask.api.base_controller import BaseController
from corpus_builder.build.application.check_status.status_checker import (
    StatusCheckerQuery,
)


status_api = Namespace("status", description="Check corpus build status")


@status_api.errorhandler(AuthorizationError)
@status_api.errorhandler(ExpiredTokenException)
def handle_authorization_error(error):
    return BaseController.api_error(error, HTTPStatus.UNAUTHORIZED)


@status_api.errorhandler(InvalidRequestParamsException)
def handle_value_error(error):
    return BaseController.api_error(error, HTTPStatus.BAD_REQUEST)


@status_api.errorhandler(Exception)
def handle_generic_error(error):
    return BaseController.api_generic_error(error)


@status_api.route("/<string:build_id>")
class GetBuildStatusController(BaseController):
    @authorization_required("check:corpus-build-status")
    def get(self, user, build_id: str):

        query = StatusCheckerQuery(build_id, user.tenant_id())

        response = self.ask(query)

        return self.response(HTTPStatus.OK, **response.to_dict())
