from flask import Flask
from flask_restx import Api
from launcher.tenant.infrastructure.persistence.sqlalchemy.mapping import LauncherOrm
from launcher.pipeline.infrastructure.controller.flask.api.pipeline import pipeline_api

from identityaccess.infrastructure.persistence.sqlalchemy.mapping import IdentityAccessOrm
from identityaccess.infrastructure.controller.flask.api.authentication import authentication_ns

from shared.infrastructure.controller.flask.api.launcher import launcher_api
from shared.infrastructure.application.settings import Settings
from shared.infrastructure.application.dependency_injection import container, event_handlers


launcher_orm = LauncherOrm()
launcher_orm.start_mappers()

identityaccess_orm = IdentityAccessOrm()
identityaccess_orm.start_mappers()

app = Flask(__name__)
app.container = container
app.event_handlers = event_handlers

api = Api(app)

app.register_blueprint(launcher_api, url_prefix=Settings.api_prefix())
app.register_blueprint(pipeline_api, url_prefix="{}/pipelines".format(Settings.api_prefix()))
api.add_namespace(authentication_ns)
