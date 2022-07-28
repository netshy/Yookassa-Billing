from environs import Env

from pydantic import BaseSettings

env = Env()
env.read_env()


class Settings(BaseSettings):
    # AMQP settings
    rabbit_host = env.str("RABBIT_HOST", "localhost")
    rabbit_port = env.str("RABBIT_PORT", "5672")

    rabbit_user = env.str("RABBIT_USER", "guest")
    rabbit_password = env.str("RABBIT_PASSWORD", "guest")

    rabbit_email_events_queue = env.str(
        "RABBIT_EVENTS_QUEUE", "notification.send-email"
    )
    rabbit_exchange = env.str("RABBIT_EXCHANGE", "notification.exchange")
    grpc_url = env.str("GRPC_URL", "grpc_auth_app:50055")

    pg_dsl = {
        "database": env.str("POSTGRES_DB", "notification_database"),
        "user": env.str("POSTGRES_USER", "app"),
        "password": env.str("POSTGRES_PASSWORD", "123qwe"),
        "host": env.str("POSTGRES_HOST", "localhost"),
        "port": env.int("POSTGRES_PORT", "5432"),
    }


config = Settings()
