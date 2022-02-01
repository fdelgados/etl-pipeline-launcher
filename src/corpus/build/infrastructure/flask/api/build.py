from flask import request
from flask_restx import Namespace, fields

from shared.infrastructure.security import authorization_required
from shared.infrastructure.flask.api.basecontroller import BaseController

from corpus.build.application.buildservice import (
    StartBuildCommand,
    BuildingProgressQuery,
    BuildingProgressResponse,
    BuildListQuery,
    BuildListResponse,
    NextIdentityQuery,
    NextIdentityResponse,
)


build_api = Namespace("build", description="Corpus build starter")

corpus = build_api.model(
    "Corpus",
    {
        "corpusName": fields.String(
            description="The name of corpus to build", required=True
        )
    },
)


@build_api.route("")
class BuildListController(BaseController):
    @authorization_required("get:corpus-build-info")
    def get(self, user):

        query = BuildListQuery(user.tenant_id())

        response: BuildListResponse = self.ask(query)

        return self.response_ok(self._serialize(response))

    def _serialize(self, response: BuildListResponse) -> dict:
        representation = {}
        build_info = []
        for build_dto in response.value():
            dto_dict = build_dto.__dict__
            dto_dict["_links"] = {
                "self": f"{self.base_url()}/builds/{build_dto.build_id}"
            }
            build_info.append(dto_dict)

        representation["data"] = build_info

        return representation

    @build_api.doc(
        description="Start a new corpus build",
        body=corpus,
        responses={
            202: "Success",
            400: "Validation Error",
            401: "Authorization failed, access token not provided or expired",
            409: "There is another build running",
        },
    )
    @authorization_required("start:corpus-build")
    def post(self, user):
        params = request.get_json()

        build_id = self._generate_build_id()

        command = StartBuildCommand(
            build_id,
            user.tenant_id(),
            user.username(),
            params.get("corpusName"),
        )

        self.dispatch(command)

        return self.response_accepted(
            headers={
                "Content-Location": f"{self.base_url()}/builds/{build_id}"
            }
        )

    def _generate_build_id(self) -> str:
        response: NextIdentityResponse = self.ask(NextIdentityQuery())

        return response.value()


@build_api.route("/<string:build_id>")
class BuildInfoController(BaseController):
    @authorization_required("get:corpus-build-info")
    def get(self, user, build_id: str):
        query = BuildingProgressQuery(user.tenant_id(), build_id)

        response: BuildingProgressResponse = self.ask(query)

        return self.response_ok(self._serialize(response))

    def _serialize(self, response: BuildingProgressResponse) -> dict:
        build_dto = response.value()

        representation = build_dto.__dict__

        representation["_links"] = {
            "self": f"{self.base_url()}/builds/{build_dto.build_id}"
        }

        return representation
