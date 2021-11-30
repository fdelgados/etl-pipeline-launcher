import os
import time

from flask import Flask
from flask_restx import Api

from shared.domain.errors.errors import ApplicationError
import shared.infrastructure.environment.globalvars as gvars
from shared.infrastructure.environment.settings import Settings
import shared.infrastructure.dic.container as container
from shared.infrastructure.flask.api.basecontroller import BaseController
from shared.application.bootstrap import Bootstrap
from shared.infrastructure.flask.api.monitoring.healthcheck import health_check
from corpus.build.infrastructure.flask.api.build import build_api
from corpus.build.infrastructure.flask.api.corpus import corpus_api
from duplicates.report.infrastructure.flask.api.report import report_api

bootstrap = Bootstrap()

app = Flask(__name__)
app.config.from_mapping(bootstrap.flask_config())


@app.before_request
def before_request_func():
    os.environ["SITE"] = "emagister.com"

    gvars.settings = Settings()
    gvars.container = container.create_container(
        gvars.settings.common_settings()
    )

    os.environ["TZ"] = gvars.settings.time_zone()
    time.tzset()


bootstrap.logger.info("Bootstrapping API")
api = Api(
    app,
    doc=bootstrap.api_doc_path(),
    title=bootstrap.api_title(),
    version=bootstrap.api_version_str(),
)


@api.errorhandler(ApplicationError)
def handle_application_error(error):
    return BaseController.api_error(error)


@api.errorhandler(Exception)
def handle_generic_error(error):
    return BaseController.api_generic_error(error)


api.add_namespace(health_check, path=bootstrap.api_prefix("monitor"))
api.add_namespace(build_api, path=bootstrap.api_prefix("builds"))
api.add_namespace(corpus_api, path=bootstrap.api_prefix("corpora"))

api.add_namespace(report_api, path=bootstrap.api_prefix("reports"))
