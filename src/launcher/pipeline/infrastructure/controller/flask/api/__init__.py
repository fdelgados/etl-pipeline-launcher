from flask_restx import Namespace
from http import HTTPStatus

from shared.infrastructure.controller.flask.api import BaseController

from shared.infrastructure.security import AuthorizationError, ExpiredTokenException
from launcher.shared.application.errors import InvalidRequestParamsException

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


@pipeline_api.errorhandler(Exception)
def handle_generic_error(error):
    return BaseController.api_generic_error(error)
