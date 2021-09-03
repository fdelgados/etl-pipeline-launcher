import os
import re
import toml
import glob
import collections

from typing import Dict, Any, Optional, List
from setuptools import find_packages


class Settings:
    def __init__(self, environment: str = 'development'):
        self._environment = environment
        self._config = toml.load('/config/settings.toml')
        environment_config = toml.load(f'/config/settings.{self._environment}.toml')

        self._dict_merge(self._config, environment_config)

        services_dir = os.path.join(self._app_root_dir(), 'config/services/')

        self._subscribed_events = {}
        subscribed_events_files = glob.glob(f'{services_dir}**/subscribed-events.toml')

        for subscribed_events_file in subscribed_events_files:
            self._dict_merge(self._subscribed_events, toml.load(subscribed_events_file))

    def _dict_merge(self, dct, merge_dct) -> None:
        for k, v in merge_dct.items():
            if k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], collections.Mapping):
                self._dict_merge(dct[k], merge_dct[k])
            else:
                dct[k] = merge_dct[k]

    def environment(self) -> str:
        return self._environment

    def is_production(self) -> bool:
        return self._environment == 'production'

    def is_development(self) -> bool:
        return self._environment == 'development'

    def flask_config(self) -> Dict:
        if not self._config.get('flask'):
            return {}

        return {key.upper(): value for (key, value) in self._config.get('flask').items()}

    def _get(self, section: str, entry: str, default: Optional[str] = None) -> Any:
        return self._config.get(section).get(entry, default)

    def application_id(self) -> str:
        return self._get('application', 'id')

    def api_version(self) -> int:
        return self._get('api', 'version')

    def api_title(self) -> str:
        return self._get('api', 'title')

    def api_doc_path(self) -> str:
        return self._get('api', 'doc_path', '/doc')

    def api_version_str(self) -> str:
        return self._get('api', 'version_str').format(self.api_version())

    def api_prefix(self, path: Optional[str] = None) -> str:
        api_prefix = self._get('api', 'prefix').format(self.api_version())
        if not path:
            return api_prefix

        return f'{api_prefix}/{path}'

    def base_url(self) -> str:
        return self._get('application', 'baseurl')

    def api_url(self) -> str:
        url = self.base_url()
        port = self._get('api', 'port')

        return "{}:{}{}".format(url, port, self.api_prefix())

    def database_dsn(self, context: str) -> str:
        database_config = self._config.get('database')
        host = database_config.get('host')

        database_config = database_config.get(context)

        return "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
            database_config.get('user'),
            database_config.get('password'),
            host,
            database_config.get('name')
        )

    def rabbit_connection_settings(self):
        return self._config.get('rabbitmq').get('connection')

    def rabbit_publish_exchange(self):
        exchanges = self._config.get('rabbitmq').get('exchanges')

        if not exchanges:
            return []

        return exchanges.get('publish')

    def rabbit_subscribe_exchanges(self):
        exchanges = self._config.get('rabbitmq').get('exchanges')

        if not exchanges:
            return []

        return exchanges.get('subscribe')

    def subscribed_events(self):
        return self._subscribed_events

    def event_subscribed_commands(self, exchange: str, event: str):
        if not self._subscribed_events:
            return {}

        return self._subscribed_events.get(exchange, {}).get(event, {})

    def _app_root_dir(self) -> str:
        return self._get('application', 'root_dir')

    def contexts(self) -> List:
        contexts_dir = self._get('application', 'contexts_dir')

        return list(filter(lambda context: '.' not in context, find_packages(where=contexts_dir)))

    def services_files(self) -> List:
        services_dir = os.path.join(self._app_root_dir(), 'config/services/')

        return glob.glob(f'{services_dir}**/*-services.xml')

    def event_handlers_file(self) -> str:
        return os.path.join(self._app_root_dir(), 'config/services/', 'event-handlers.xml')

    def public_key(self) -> str:
        with open(self._get('identity_access', 'public_key_file')) as fp:
            return fp.read()

    def token_issuer(self) -> str:
        return self._get('identity_access', 'token_issuer')

    def db_mapping_classes(self):
        src_dir = os.path.join(self._app_root_dir(), 'src')

        context_mapping_files = {}
        mapping_modules = []
        for context in self.contexts():
            mapping_files = glob.glob(f'{src_dir}/{context}/infrastructure/persistence/sqlalchemy/mapping.py')
            mapping_files.extend(glob.glob(f'{src_dir}/{context}/**/infrastructure/persistence/sqlalchemy/mapping.py'))
            context_mapping_files[context] = mapping_files

        for context, files in context_mapping_files.items():
            for file in files:
                module_name = file.replace(f'{src_dir}/', '').replace('/', '.')
                module_name = re.sub(r'\.py$', '', module_name)
                module_name = '{}.{}Mapping'.format(module_name, context.capitalize())
                mapping_modules.append(module_name)

        return mapping_modules

    def api_path(self):
        return "/{}".format(self.api_version())

    def logs_dir(self):
        return self._get('application', 'logs_dir')

    def templates_dir(self):
        return self._get('application', 'templates_dir')

    def assets_dir(self):
        return self._get('application', 'assets_dir')


settings = Settings(os.environ.get('FLASK_ENV', 'development'))
