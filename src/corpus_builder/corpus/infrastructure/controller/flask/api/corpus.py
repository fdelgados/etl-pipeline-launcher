from http import HTTPStatus
from flask import request
from flask_restx import Namespace

from shared import InvalidRequestParamsException
from shared.infrastructure.security import (
    authorization_required,
    AuthorizationError,
    ExpiredTokenException,
)
from shared.infrastructure.controller.flask.api import BaseController
from corpus_builder.corpus.application.create.corpus_creator import CorpusCreatorCommand

corpus_api = Namespace("corpus", description="Create/Update corpus")


@corpus_api.errorhandler(AuthorizationError)
@corpus_api.errorhandler(ExpiredTokenException)
def handle_authorization_error(error):
    return BaseController.api_error(error, HTTPStatus.UNAUTHORIZED)


@corpus_api.errorhandler(InvalidRequestParamsException)
def handle_value_error(error):
    return BaseController.api_error(error, HTTPStatus.BAD_REQUEST)


# @corpus_api.errorhandler(Exception)
# def handle_authorization_error(error):
#     return BaseController.api_generic_error(error)


@corpus_api.route("/<string:name>")
class PutCorpusController(BaseController):
    @authorization_required("create:corpus")
    def put(self, user, name):
        params = request.get_json()

        command = CorpusCreatorCommand(
            user.tenant_id(),
            name,
            params.get("sitemaps"),
            params.get("customRequestHeaders"),
            params.get("selectorMapping"),
            params.get("excludedTags"),
            params.get("excludedSelectors"),
            params.get("description"),
            params.get("customFields"),
            params.get("urlPattern"),
        )

        self.dispatch(command)

        return self.response(HTTPStatus.CREATED)
