import os
import glob
import collections
from typing import Dict, Any, Optional, List
import toml

from setuptools import find_packages


class Settings:
    def __init__(self):
        self._environment = os.environ.get("ENVIRONMENT", "development")
        self._site = os.environ.get("SITE")

        settings_dir = Settings.settings_dir()
        services_dir = f"{Settings.configs_dir()}/services"

        self._config = Settings.common_settings()
        common_environment_config = toml.load(
            f"{settings_dir}/common/settings.{self._environment}.toml"
        )

        self._dict_merge(self._config, common_environment_config)

        if not self.is_test():
            site_config = toml.load(
                f"{settings_dir}/{self._site}/settings.toml"
            )
            self._dict_merge(self._config, site_config)

            site_env_file = "{}/{}/settings.{}.toml".format(
                settings_dir,
                self._site,
                self._environment,
            )

            if os.path.isfile(site_env_file):
                site_environment_config = toml.load(site_env_file)

                self._dict_merge(self._config, site_environment_config)

        self._subscribed_events = {}
        subscribed_events_files = glob.glob(
            f"{services_dir}/**/subscribed-events.toml"
        )

        for subscribed_events_file in subscribed_events_files:
            self._dict_merge(
                self._subscribed_events, toml.load(subscribed_events_file)
            )

        self._commands = {}
        commands_files = glob.glob(f"{services_dir}/**/commands.toml")
        for commands_file in commands_files:
            self._dict_merge(self._commands, toml.load(commands_file))

        os.environ["TZ"] = self.time_zone()

    def _dict_merge(self, dct, merge_dct) -> None:
        for key in merge_dct.keys():
            if (
                key in dct
                and isinstance(dct[key], dict)
                and isinstance(merge_dct[key], collections.abc.Mapping)
            ):
                self._dict_merge(dct[key], merge_dct[key])
            else:
                dct[key] = merge_dct[key]

    @staticmethod
    def common_settings() -> dict:
        return toml.load(f"{Settings.settings_dir()}/common/settings.toml")

    def environment_settings(self) -> dict:
        common_settings = Settings.common_settings()

        settings_dir = Settings.settings_dir()
        environment = self.environment()
        environment_settings = toml.load(
            f"{settings_dir}/common/settings.{environment}.toml"
        )

        self._dict_merge(environment_settings, common_settings)

        return environment_settings

    @staticmethod
    def configs_dir() -> str:
        return "/opt/code/config"

    @staticmethod
    def settings_dir() -> str:
        return f"{Settings.configs_dir()}/settings"

    def services_files(self) -> List:
        services_dir = os.path.join(self._configs_dir(), "services/")

        return glob.glob(f"{services_dir}**/*-services.xml")

    def event_handlers_files(self) -> str:
        services_dir = os.path.join(self._configs_dir(), "services/")

        return glob.glob(f"{services_dir}**/event-handlers.xml")

    def environment(self) -> str:
        return self._environment

    def is_production(self) -> bool:
        return self._environment == "production"

    def is_development(self) -> bool:
        return self._environment == "development"

    def is_test(self) -> bool:
        return self._environment == "test"

    def site(self) -> str:
        return self._site

    def _get(
        self, section: str, entry: str, default: Optional[Any] = None
    ) -> Any:
        return self._config.get(section).get(entry, default)

    def application_id(self) -> str:
        return self._get("application", "id")

    def api_title(self) -> str:
        return self._get("api", "title")

    def api_version(self) -> int:
        return self._get("api", "version")

    def api_doc_path(self) -> str:
        return self._get("api", "doc_path", "/doc")

    def api_version_str(self) -> str:
        return self._get("api", "version_str").format(self.api_version())

    def api_prefix(self, path: Optional[str] = None) -> str:
        api_prefix = self._get("api", "prefix").format(self.api_version())
        if not path:
            return api_prefix

        return f"{api_prefix}/{path}"

    def base_url(self) -> str:
        return self._get("application", "baseurl")

    def api_port(self) -> str:
        return str(self._get("api", "port"))

    def api_url(self) -> str:
        url = self.base_url()
        port = self._get("api", "port")

        return "{}:{}{}".format(url, port, self.api_prefix())

    def rabbit_publish_exchange(self):
        exchanges = self._config.get("rabbitmq").get("exchanges")

        if not exchanges:
            return []

        return exchanges.get("publish")

    def subscribed_events(self):
        return self._subscribed_events

    def event_subscribed_commands(self, exchange: str, event: str):
        if not self._subscribed_events:
            return {}

        return self._subscribed_events.get(exchange, {}).get(event, {})

    def redis_host(self):
        return os.environ.get("REDIS_HOST")

    def redis_port(self):
        return os.environ.get("REDIS_PORT")

    def redis_database(self, database: str) -> int:
        databases = self._get("redis", "databases")

        database_number = databases.get(database)

        if not database_number:
            raise ValueError(f"{database} database does not exist")

        return database_number

    def command(self, command: str):
        return self._commands.get("commands", {}).get(command)

    def get_app_root_dir(self) -> str:
        return self._get("application", "root_dir")

    def contexts_dir(self) -> str:
        return self._get("application", "contexts_dir")

    def contexts(self) -> List:
        return list(
            filter(
                lambda context: "." not in context,
                find_packages(where=self.contexts_dir()),
            )
        )

    def public_key(self) -> str:
        with open(
            self._get("identity_access", "public_key_file"), encoding="utf8"
        ) as fp:
            return fp.read()

    def token_issuer(self) -> str:
        return self._get("identity_access", "token_issuer")

    def verify_token_expiration_time(self) -> bool:
        return self._get("identity_access", "verify_token_expiration_time")

    def event_store_config_for_context(self, context: str) -> Dict:
        context_config = self._get("application", "contexts", {}).get(context)

        if not context_config:
            return {}

        return context_config.get("event_store", {})

    def store_domain_even_subscriber(self) -> Dict:
        return self._config.get("application").get(
            "store_domain_event_subscriber"
        )

    def is_event_store_enabled_for_context(self, context: str) -> bool:
        context_event_store = self.event_store_config_for_context(context)

        if not context_event_store:
            return False

        return context_event_store.get("enabled", False)

    def event_store_id(self, context: str) -> Optional[str]:
        context_event_store = self.event_store_config_for_context(context)

        if not context_event_store:
            return None

        return context_event_store.get("id")

    def duplicates_content_file(self, tenant_id: str) -> str:
        file_pattern = self._get("duplicates", "content_file")

        return file_pattern.format(tenant_id, self._site)

    def duplicates_minhashes_file(self, tenant_id: str) -> str:
        file_pattern = self._get("duplicates", "minhashes_file")

        return file_pattern.format(tenant_id, self._site)

    def api_path(self):
        return "/{}".format(self.api_version())

    def _configs_dir(self):
        return self._get("application", "configs_dir")

    def templates_dir(self):
        return self._get("application", "templates_dir")

    def assets_dir(self):
        return self._get("application", "assets_dir")

    def time_zone(self):
        return self._get("application", "timezone")

    def flask_config(self) -> Dict:
        if not self._config.get("flask"):
            return {}

        return {
            key.upper(): value
            for (key, value) in self._config.get("flask").items()
        }

    def database_dsn(self, context: str) -> str:
        context = context.upper()

        db_user = f"{context}_{self._env_site()}_DATABASE_USER"
        db_password = f"{context}_{self._env_site()}_DATABASE_PASSWORD"
        db_name = f"{context}_{self._env_site()}_DATABASE_NAME"

        return "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
            os.environ.get(db_user),
            os.environ.get(db_password),
            os.environ.get("MARIA_DB_HOST"),
            os.environ.get(db_name),
        )

    def mongodb_connection_settings(self) -> dict:
        db_user = f"MONGO_{self._env_site()}_INITDB_USER"
        db_password = f"MONGO_{self._env_site()}_INITDB_PASSWORD"
        db_name = f"MONGO_{self._env_site()}_INITDB_DATABASE"

        return {
            "host": os.environ.get("MONGO_HOST"),
            "port": int(os.environ.get("MONGO_PORT")),
            "username": os.environ.get(db_user),
            "password": os.environ.get(db_password),
            "database": os.environ.get(db_name),
        }

    def _env_site(self) -> str:
        return self._site.replace(".", "_").upper()

    def rabbit_connection_settings(self) -> dict:
        return {
            "host": os.environ.get("RABBITMQ_HOST"),
            "port": os.environ.get("RABBITMQ_PORT"),
            "user": os.environ.get("RABBITMQ_USER"),
            "password": os.environ.get("RABBITMQ_PASSWORD"),
            "vhost": "/",
        }
