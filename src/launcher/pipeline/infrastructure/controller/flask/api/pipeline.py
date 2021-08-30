from flask import make_response, request
from flask_restx import Namespace
from http import HTTPStatus

from shared.infrastructure.controller.flask.api import BaseController

from shared.infrastructure.security import AuthorizationError, ExpiredTokenException
from shared import settings
from launcher.shared.application.errors import InvalidRequestParamsException
from launcher.pipeline.application.launch_pipeline import LaunchPipeline, LaunchPipelineCommand

pipeline_api = Namespace(
    'pipeline',
    description='ETL pipeline launcher'
)


@pipeline_api.errorhandler(AuthorizationError)
@pipeline_api.errorhandler(ExpiredTokenException)
def handle_authorization_error(error):
    return BaseController.api_error(error, HTTPStatus.UNAUTHORIZED)


@pipeline_api.errorhandler(InvalidRequestParamsException)
def handle_value_error(error):
    return BaseController.api_error(error, HTTPStatus.BAD_REQUEST)


@pipeline_api.route('')
class PipelineController(BaseController):
    def post(self):
        params = request.get_json()

        command = LaunchPipelineCommand(
            params.get("sitemapUrl"),
            params.get("customRequestHeaders"),
            params.get("selectorMapping"),
            params.get("excludedSelectors"),
            params.get("description"),
            params.get("customFields")
        )

        launcher_service: LaunchPipeline = self.service(
            'launcher.pipeline.application.launch_pipeline.launch_pipeline'
        )

        pipeline_id = launcher_service.execute(command)

        response = make_response("", HTTPStatus.ACCEPTED)
        response.headers["Location"] = "{}/corpora/{}".format(settings.api_url(), pipeline_id)

        return response
