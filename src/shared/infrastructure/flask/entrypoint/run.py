from flask import Flask
from flask_restx import Api

from shared import Bootstrap, settings
from corpus_builder.build.infrastructure.flask.api.build import build_api
from corpus_builder.build.infrastructure.flask.api.status import status_api
from corpus_builder.corpus.infrastructure.flask.api.corpus import corpus_api
from duplicates.report.infrastructure.flask.api.report import report_api


bootstrap = Bootstrap()
bootstrap.generate_db_maps()

app = Flask(__name__)
app.config.from_mapping(settings.flask_config())

bootstrap.logger.info("Bootstrapping API")
api = Api(
    app,
    doc=settings.api_doc_path(),
    title=settings.api_title(),
    version=settings.api_version_str(),
)

api.add_namespace(build_api, path=settings.api_prefix("builds"))
api.add_namespace(status_api, path=settings.api_prefix("builds"))
api.add_namespace(corpus_api, path=settings.api_prefix("corpora"))

api.add_namespace(report_api, path=settings.api_prefix("reports"))
