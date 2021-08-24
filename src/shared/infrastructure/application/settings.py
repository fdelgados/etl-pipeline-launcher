import os
import toml
import glob
from setuptools import find_packages


class Settings:
    def __init__(self, environment: str = 'development'):
        self._config = toml.load('/config/settings.toml')
        self._environment = environment

    def _get(self, section: str, entry: str):
        config = self._config.get(section)

        if self._environment == 'development':
            return config.get(entry)

        return config.get(self._environment).get(entry)

    def application_id(self):
        return self._config.get('application').get('id')

    def api_version(self):
        return self._config.get('api').get('version')

    def api_title(self):
        return self._config.get('api').get('title')

    def api_doc_path(self):
        return self._config.get('api').get('doc_path', '/doc')

    def api_version_str(self):
        return self._config.get('api').get('version_str').format(self.api_version())

    def api_prefix(self, path: str = None):
        api_prefix = self._config.get('api').get('prefix').format(self.api_version())
        if not path:
            return api_prefix

        return f'{api_prefix}/{path}'

    def base_url(self):
        return self._config.get('application').get(self._environment).get('baseurl')

    def api_url(self):
        url = self.base_url()
        port = self._config.get('api').get('port')

        return "{}:{}{}".format(url, port, self.api_prefix())

    def database_dsn(self, context: str):
        database_config = self._config.get('database').get(self._environment).get(context)

        return "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
            database_config.get('user'),
            database_config.get('password'),
            database_config.get('host'),
            database_config.get('name')
        )

    def _app_root_dir(self):
        return self._config.get('application').get('root_dir')

    def contexts(self):
        contexts_dir = self._config.get('application').get('contexts_dir')

        return list(filter(lambda context: '.' not in context, find_packages(where=contexts_dir)))

    def services_files(self):
        services_dir = os.path.join(self._app_root_dir(), 'config/services/')

        return glob.glob(f'{services_dir}**/*-services.xml')

    def event_handlers_file(self):
        return os.path.join(self._app_root_dir(), 'config/services/', 'event-handlers.xml')

    def public_key(self):
        identity_access_config = self._config.get('identity_access').get(self._environment)

        with open(identity_access_config.get('public_key_file')) as fp:
            return fp.read()

    def token_issuer(self):
        identity_access_config = self._config.get('identity_access').get(self._environment)

        return identity_access_config.get('token_issuer')


    def mapping_class_pattern(self):
        return "infrastructure.persistence.sqlalchemy.mapping.{}.{}Orm"

    def api_path(self):
        return "/{}".format(self.api_version())


settings = Settings(os.environ.get('FLASK_ENV'))
