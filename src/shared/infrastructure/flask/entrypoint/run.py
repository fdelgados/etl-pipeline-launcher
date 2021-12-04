from flask import Flask
from flask_restx import Api

from shared.domain.errors.errors import ApplicationError
import shared.infrastructure.environment.globalvars as global_vars
from shared.infrastructure.flask.api.basecontroller import BaseController
from shared.application.bootstrap import Bootstrap
from shared.infrastructure.flask.api.monitoring.healthcheck import health_check
from corpus.build.infrastructure.flask.api.build import build_api
from corpus.build.infrastructure.flask.api.corpus import corpus_api
from duplicates.report.infrastructure.flask.api.report import report_api

bootstrap = Bootstrap()

app = Flask(__name__)
app.config.from_mapping(global_vars.settings.flask_config())

#
# @app.before_request
# def before_request_func():
#     site = request.headers.get("Site")
#     os.environ["SITE"] = site
#
#     global_vars.settings = Settings()
#     global_vars.container = container.create_container(
#         global_vars.settings.common_settings()
#     )
#
#     os.environ["TZ"] = global_vars.settings.time_zone()
#     time.tzset()


bootstrap.logger.info("Bootstrapping API")
api = Api(
    app,
    doc=global_vars.settings.api_doc_path(),
    title=global_vars.settings.api_title(),
    version=global_vars.settings.api_version_str(),
)


@api.errorhandler(ApplicationError)
def handle_application_error(error):
    return BaseController.api_error(error)


@api.errorhandler(Exception)
def handle_generic_error(error):
    return BaseController.api_generic_error(error)


api.add_namespace(
    health_check, path=global_vars.settings.api_prefix("monitor")
)
api.add_namespace(build_api, path=global_vars.settings.api_prefix("builds"))
api.add_namespace(corpus_api, path=global_vars.settings.api_prefix("corpora"))

api.add_namespace(report_api, path=global_vars.settings.api_prefix("reports"))
