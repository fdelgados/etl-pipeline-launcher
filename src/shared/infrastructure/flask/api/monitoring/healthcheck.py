from datetime import datetime
from flask_restx import Namespace

import shared.infrastructure.environment.globalvars as glob

from shared.infrastructure.flask.api.basecontroller import BaseController


health_check = Namespace("health_check", description="Health check endpoint")


@health_check.route("/health-check")
class HealthCheckController(BaseController):
    def get(self):
        return self.response_ok({
            "status": "OK",
            "version": glob.settings.api_version(),
            "date": datetime.now(),
        })
