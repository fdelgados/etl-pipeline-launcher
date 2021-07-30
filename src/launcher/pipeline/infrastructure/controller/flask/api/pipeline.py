from flask import make_response, request, jsonify, current_app, Blueprint
from http import HTTPStatus

from shared_context.infrastructure.api.flask import error_response

from shared.infrastructure.security.authentication import authentication_required, AuthenticationError
from shared.infrastructure.application.settings import Settings
from shared.application.errors import ErrorCodes, InvalidRequestParamsException
from launcher.tenant.domain.errors import TenantNotFoundException
from launcher.pipeline.application.launcher import LaunchPipeline, LaunchPipelineCommand

pipeline_api = Blueprint("pipeline_api", __name__)


@pipeline_api.route("", methods=["POST"])
@authentication_required
def launch_pipeline(tenant_id: str):
    params = request.get_json()

    command = LaunchPipelineCommand(
        tenant_id,
        params.get("sitemapUrl"),
        params.get("customRequestHeaders"),
        params.get("selectorMapping"),
        params.get("excludedSelectors"),
        params.get("description"),
        params.get("customFields")
    )

    launcher_service: LaunchPipeline = current_app.container.get(
        "launcher.launcher.pipeline.application.launcher.launch_pipeline"
    )

    try:
        pipeline_id = launcher_service.handle(command)
    except InvalidRequestParamsException as e:
        return error_response(e.code, e.message, status=HTTPStatus.BAD_REQUEST)
    except TenantNotFoundException as e:
        return error_response(
            ErrorCodes.TENANT_NOT_FOUND,
            "{}. {}".format(str(ErrorCodes.TENANT_NOT_FOUND), str(e)),
            status=HTTPStatus.FORBIDDEN
        )
    except AuthenticationError as e:
        return error_response(
            ErrorCodes.AUTHENTICATION_FAILED,
            "{}. {}".format(str(ErrorCodes.AUTHENTICATION_FAILED), str(e)),
            status=HTTPStatus.UNAUTHORIZED
        )

    response = make_response("", 202)
    response.headers["Location"] = "{}/corpora/{}".format(Settings.api_url(), pipeline_id)

    return response
