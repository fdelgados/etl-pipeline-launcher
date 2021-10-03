from http import HTTPStatus
from flask import request, make_response
from flask_restx import Namespace

import shared.infrastructure.environment.globalvars as glob
from shared.infrastructure.security import authorization_required
from shared.infrastructure.flask.api.basecontroller import BaseController
from corpus.build.application.build_starter import StartBuildCommand
from corpus.build.application.identity_generator import (
    NextIdentityQuery,
    NextIdentityResponse,
)
from corpus.build.application.build_info_retriever import (
    RetrieveBuildInfoQuery,
    RetrieveBuildInfoResponse,
)


build_api = Namespace("build", description="Corpus build starter")


@build_api.route("")
class StartBuildController(BaseController):
    @authorization_required("start:corpus-build")
    def post(self, user):
        params = request.get_json()

        build_id = self._generate_build_id()

        command = StartBuildCommand(
            build_id, user.tenant_id(), user.username(), params.get("corpusName")
        )

        self.dispatch(command)

        response = make_response("", HTTPStatus.ACCEPTED)
        response.headers = {
            "Content-Location": f"{glob.settings.api_url()}/builds/{build_id}"
        }

        return response

    def _generate_build_id(self) -> str:
        response: NextIdentityResponse = self.ask(NextIdentityQuery())

        return response.build_id


@build_api.route("")
class BuildListController(BaseController):
    @authorization_required("get:corpus-build-info")
    def get(self, user):

        query = RetrieveBuildInfoQuery(user.tenant_id())

        response: RetrieveBuildInfoResponse = self.ask(query)

        build_info = []
        for dto in response.build_info_dtos:
            dto_dict = dto.to_dict()
            dto_dict["links"] = {
                "self": f"{glob.settings.api_url()}/builds/{dto.build_id}"
            }
            build_info.append(dto_dict)

        return make_response(
            self.json_response(*build_info),
            HTTPStatus.OK,
        )


@build_api.route("/<string:build_id>")
class BuildInfoController(BaseController):
    @authorization_required("get:corpus-build-info")
    def get(self, user, build_id: str):

        query = RetrieveBuildInfoQuery(user.tenant_id(), build_id)

        response: RetrieveBuildInfoResponse = self.ask(query)
        build = response.build_info_dtos[0]

        links = {"self": f"{glob.settings.api_url()}/builds/{build_id}"}

        return make_response(
            self.json_response(**build.to_dict(), _links=links), HTTPStatus.OK
        )
