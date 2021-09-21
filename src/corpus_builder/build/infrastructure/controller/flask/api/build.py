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
from corpus_builder.build.application.start.start_build import BuildStarter, BuildStarterCommand


build_api = Namespace("build", description="Corpus build starter")


@build_api.errorhandler(AuthorizationError)
@build_api.errorhandler(ExpiredTokenException)
def handle_authorization_error(error):
    return BaseController.api_error(error, HTTPStatus.UNAUTHORIZED)


@build_api.errorhandler(InvalidRequestParamsException)
def handle_value_error(error):
    return BaseController.api_error(error, HTTPStatus.BAD_REQUEST)


@build_api.route("")
class BuildController(BaseController):
    @authorization_required("start:corpus-build")
    def post(self, user):
        params = request.get_json()

        command = BuildStarterCommand(
            user.tenant_id(),
            user.username(),
            params.get("corpusName")
        )

        build_starter: BuildStarter = self.service(
            "corpus_builder.build.application.start.start_build.build_starter"
        )

        build_id = build_starter.start(command)

        return self.response(
            HTTPStatus.ACCEPTED,
            {"Location": f"{settings.api_url()}/builds/{build_id}"}
        )

    def get(self):
        pass
