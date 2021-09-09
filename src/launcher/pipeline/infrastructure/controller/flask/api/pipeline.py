from flask import make_response, request
from http import HTTPStatus

from shared.infrastructure.controller.flask.api import BaseController

from shared import settings
from launcher.pipeline.application.launch.pipeline_launcher import PipelineLauncher, PipelineLauncherCommand

from . import pipeline_api


@pipeline_api.route('')
class PipelineController(BaseController):
    def post(self):
        params = request.get_json()

        command = PipelineLauncherCommand(
            params.get("sitemaps"),
            params.get("customRequestHeaders"),
            params.get("selectorMapping"),
            params.get("excludedTags"),
            params.get("excludedSelectors"),
            params.get("description"),
            params.get("customFields"),
            params.get("urlPattern")
        )

        launcher_service: PipelineLauncher = self.service(
            'launcher.pipeline.application.launch.pipeline_launcher.pipeline_launcher'
        )

        pipeline_id = launcher_service.execute(command)

        response = make_response("", HTTPStatus.ACCEPTED)
        response.headers["Location"] = "{}/pipelines/{}".format(settings.api_url(), pipeline_id)

        return response
