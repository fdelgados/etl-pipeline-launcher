from flask import Flask
from flask_restx import Api

from bootstrap import Bootstrap
from corpus.etl.infrastructure.controller.flask.api.etl import etl_api

# from corpus.shared.infrastructure.controller.flask.api import launcher_api, Launcher
from shared import settings


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
# api.add_namespace(launcher_api, path=settings.api_prefix())
api.add_namespace(etl_api, path=settings.api_prefix("etls"))
