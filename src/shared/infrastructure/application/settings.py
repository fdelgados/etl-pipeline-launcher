import os


class Settings:
    @staticmethod
    def api_prefix():
        return os.environ.get("API_PREFIX")

    @staticmethod
    def api_url():
        url = os.environ.get("APP_URL")
        port = os.environ.get("APP_PORT")

        return "{}:{}{}".format(url, port, Settings.api_prefix())

    @staticmethod
    def database_dsn():
        host = os.environ.get("DB_HOST")
        user = os.environ.get("DB_USER")
        database = os.environ.get("DB_NAME")
        password = os.environ.get("DB_PASSWORD")

        return "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
            user,
            password,
            host,
            database
        )

    @staticmethod
    def _app_root_dir():
        return os.environ.get("ROOT_DIR")

    @staticmethod
    def services_file():
        return os.path.join(
            Settings._app_root_dir(),
            "config/services/",
            "services.xml"
        )

    @staticmethod
    def event_handlers_file():
        return os.path.join(
            Settings._app_root_dir(),
            "config/services/",
            "event-handlers.xml"
        )

    @staticmethod
    def secret_key():
        return os.environ.get("SECRET_KEY")

    @staticmethod
    def mapping_class_pattern():
        return "infrastructure.persistence.sqlalchemy.mapping.{}.{}Orm"

    @staticmethod
    def api_path():
        api_version = os.environ.get("API_VERSION", "v1")

        return "/{}".format(api_version)
