from flask import make_response, request
from flask_restx import Namespace
from http import HTTPStatus

from shared import settings, InvalidRequestParamsException
from shared.infrastructure.security import AuthorizationError, ExpiredTokenException
from shared.infrastructure.controller.flask.api import BaseController
from corpus.etl.application.start.start_etl import EtlStarter, EtlStarterCommand


etl_api = Namespace("etl", description="ETL pipeline starter")


@etl_api.errorhandler(AuthorizationError)
@etl_api.errorhandler(ExpiredTokenException)
def handle_authorization_error(error):
    return BaseController.api_error(error, HTTPStatus.UNAUTHORIZED)


@etl_api.errorhandler(InvalidRequestParamsException)
def handle_value_error(error):
    return BaseController.api_error(error, HTTPStatus.BAD_REQUEST)


@etl_api.route("")
class EtlController(BaseController):
    def post(self):
        params = request.get_json()

        command = EtlStarterCommand(
            params.get("sitemaps"),
            params.get("customRequestHeaders"),
            params.get("selectorMapping"),
            params.get("excludedTags"),
            params.get("excludedSelectors"),
            params.get("description"),
            params.get("customFields"),
            params.get("urlPattern"),
        )

        launcher_service: EtlStarter = self.service(
            "corpus.etl.application.start.start_etl.etl_starter"
        )

        etl_id = launcher_service.start(command)

        response = make_response("", HTTPStatus.ACCEPTED)
        response.headers["Location"] = "{}/etls/{}".format(settings.api_url(), etl_id)

        return response
