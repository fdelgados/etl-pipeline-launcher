from flask import Flask
from flask_restx import Api
from pydic import create_container
from launcher.pipeline.infrastructure.controller.flask.api.pipeline import pipeline_api
from launcher.pipeline.infrastructure.persistence.sqlalchemy.mapping import LauncherOrm

from shared.infrastructure.controller.flask.api.launcher import launcher_api
from shared.infrastructure.application.settings import settings


launcher_orm = LauncherOrm()
launcher_orm.start_mappers()

app = Flask(__name__)
app.container = create_container(
    settings.services_files(),
    settings.event_handlers_file()
)

app.config['ERROR_INCLUDE_MESSAGE'] = False

api = Api(
    app,
    doc=settings.api_doc_path(),
    title=settings.api_title(),
    version=settings.api_version_str()
)
api.add_namespace(launcher_api, path=settings.api_prefix())
api.add_namespace(pipeline_api, path=settings.api_prefix('pipelines'))
