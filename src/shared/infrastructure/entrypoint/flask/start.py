from importlib import util
from flask import Flask
from flask_restx import Api
from pydic import create_container
from launcher.pipeline.infrastructure.controller.flask.api.pipeline import pipeline_api

from launcher.shared.infrastructure.controller.flask.api import launcher_api
from shared import settings


def _generate_db_maps():
    contexts = settings.contexts()
    orm_file_pattern = settings.mapping_class_pattern()

    for context in contexts:
        module_name, class_name = orm_file_pattern.format(context, context.capitalize()).rsplit('.', 1)

        try:
            spec = util.find_spec(module_name)
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)

            class_ = getattr(module, class_name)
            mapper = class_()
            mapper.start_mappers()
        except (ModuleNotFoundError, AttributeError):
            continue


_generate_db_maps()

app = Flask(__name__)
app.container = create_container(
    settings.services_files(),
    settings.event_handlers_file()
)
app.config.from_mapping(settings.flask_config())

api = Api(
    app,
    doc=settings.api_doc_path(),
    title=settings.api_title(),
    version=settings.api_version_str()
)
api.add_namespace(launcher_api, path=settings.api_prefix())
api.add_namespace(pipeline_api, path=settings.api_prefix('pipelines'))
