import os
import requests
import pytest
import time

from pathlib import Path

from tenacity import retry, stop_after_delay

from shared.infrastructure.environment.settings import Settings

settings = Settings(
    os.environ.get("SITE"),
    os.environ.get("ENVIRONMENT", "development"),
)


@retry(stop=stop_after_delay(10))
def wait_for_webapp_to_come_up():
    # base_url = settings.base_url()
    base_url = "http://nlp-emagistercom"
    api_prefix = settings.api_prefix("monitor")
    api_port = settings.api_port()

    return requests.get(f"{base_url}:{api_port}{api_prefix}/health-check")


@pytest.fixture
def restart_api():
    (Path(settings.get_app_entry_point())).touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()
