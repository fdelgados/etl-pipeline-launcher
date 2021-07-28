from flask import Flask
# from infrastructure.persistence.sqlalchemy.orm import LauncherOrm
# from bootstrap import create_container, get_event_handlers
from infrastructure.controller.flask.api.launcher import api_launcher

# launcher_orm = LauncherOrm()
# launcher_orm.start_mappers()

app = Flask(__name__)

app.register_blueprint(api_launcher)
# bootstrap()

# container = create_container()
# event_handlers = get_event_handlers()

