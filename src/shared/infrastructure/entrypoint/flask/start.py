from flask import Flask
from flask_restx import Api

from launcher.pipeline.infrastructure.controller.flask.api.pipeline import pipeline_api

from launcher.shared.infrastructure.controller.flask.api import launcher_api, Launcher
from shared import settings

from bootstrap import Bootstrap

bootstrap = Bootstrap()
bootstrap.generate_db_maps()

app = Flask(__name__)
app.config.from_mapping(settings.flask_config())

bootstrap.logger.info('Bootstrapping API')
api = Api(
    app,
    doc=settings.api_doc_path(),
    title=settings.api_title(),
    version=settings.api_version_str()
)
api.add_namespace(launcher_api, path=settings.api_prefix())
api.add_namespace(pipeline_api, path=settings.api_prefix('pipelines'))
