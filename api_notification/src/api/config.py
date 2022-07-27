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

    welcome_template_id = env.str(
        "WELCOME_TEMPLATE_ID", "aec5e982-e5b8-48fc-9ed6-15edc00b50c5"
    )


config = Settings()
