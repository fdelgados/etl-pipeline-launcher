from http import HTTPStatus
from flask import request
from flask_restx import Namespace

from shared import settings, InvalidRequestParamsException
from shared.infrastructure.security import (
    authorization_required,
    AuthorizationError,
    ExpiredTokenException,
)
from shared.infrastructure.controller.flask.api import BaseController
from corpus_builder.build.application.start.start_build import StartBuildCommand
from corpus_builder.build.application.identity.next_identity import (
    NextIdentityQuery,
    NextIdentityResponse,
)


build_api = Namespace("build", description="Corpus build starter")


@build_api.errorhandler(AuthorizationError)
@build_api.errorhandler(ExpiredTokenException)
def handle_authorization_error(error):
    return BaseController.api_error(error, HTTPStatus.UNAUTHORIZED)


@build_api.errorhandler(InvalidRequestParamsException)
def handle_value_error(error):
    return BaseController.api_error(error, HTTPStatus.BAD_REQUEST)


@build_api.route("")
class PostBuildController(BaseController):
    @authorization_required("start:corpus-build")
    def post(self, user):
        params = request.get_json()

        build_id = self._generate_build_id()

        command = StartBuildCommand(
            build_id, user.tenant_id(), user.username(), params.get("corpusName")
        )

        self.dispatch(command)

        return self.response(
            HTTPStatus.ACCEPTED, {"Location": f"{settings.api_url()}/builds/{build_id}"}
        )

    def _generate_build_id(self) -> str:
        response: NextIdentityResponse = self.ask(NextIdentityQuery())

        return response.build_id
