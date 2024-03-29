from http import HTTPStatus
from flask import request, make_response
from flask_restx import Namespace

from shared.infrastructure.security import authorization_required
from shared.infrastructure.flask.api.basecontroller import BaseController
from corpus.build.application.corpus_creator import CorpusCreatorCommand

corpus_api = Namespace("corpus", description="Create/Update corpus")


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
