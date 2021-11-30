import os


class Environment:
    @staticmethod
    def database_dsn(context: str) -> str:
        context = context.upper()

        db_user = f"{context}_{Environment._site()}_DATABASE_USER"
        db_password = f"{context}_{Environment._site()}_DATABASE_PASSWORD"
        db_name = f"{context}_{Environment._site()}_DATABASE_NAME"

        return "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
            os.environ.get(db_user),
            os.environ.get(db_password),
            os.environ.get("MARIA_DB_HOST"),
            os.environ.get(db_name),
        )

    @staticmethod
    def mongodb_connection_settings() -> dict:
        db_user = f"MONGO_{Environment._site()}_INITDB_USER"
        db_password = f"MONGO_{Environment._site()}_INITDB_PASSWORD"
        db_name = f"MONGO_{Environment._site()}_INITDB_DATABASE"

        return {
            "host": os.environ.get("MONGO_HOST"),
            "port": int(os.environ.get("MONGO_PORT")),
            "username": db_user,
            "password": db_password,
            "database": db_name,
        }

    @staticmethod
    def rabbit_connection_settings() -> dict:
        return {
            "host": os.environ.get("RABBITMQ_HOST"),
            "port": os.environ.get("RABBITMQ_PORT"),
            "user": os.environ.get("RABBITMQ_USER"),
            "password": os.environ.get("RABBITMQ_PASSWORD"),
            "vhost": "/",
        }

    @staticmethod
    def _site() -> str:
        site = os.environ.get("SITE")

        return site.replace(".", "_").upper()
