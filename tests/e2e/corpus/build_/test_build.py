import unittest

import pytest
import requests

from shared.infrastructure.environment.settings import Settings


class TestBuild(unittest.TestCase):
    _settings = None

    def setUp(self) -> None:
        self._settings = Settings()

    @pytest.mark.usefixtures("restart_api")
    def test_foo(self) -> None:
        api_url = self._settings.api_url()
        requests.get(api_url)
