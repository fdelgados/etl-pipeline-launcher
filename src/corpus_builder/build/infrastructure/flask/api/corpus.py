from http import HTTPStatus
from flask import request, make_response
from flask_restx import Namespace

from shared.infrastructure.security import authorization_required
from shared.infrastructure.flask.api.base_controller import BaseController
from corpus_builder.build.application.corpus_creator import CorpusCreatorCommand

corpus_api = Namespace("corpus_builder", description="Create/Update corpus_builder")


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

        return make_response("", HTTPStatus.CREATED)
