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
    payment_ok_template_id = env.str(
        "PAYMENT_OK_TEMPLATE_ID", "de861988-861b-4b46-9da0-b6214c6bf2e5"
    )
    payment_fail_template_id = env.str(
        "PAYMENT_FAIL_TEMPLATE_ID", "c754b482-f6cf-40b7-9c37-0d4eced5e24e"
    )
    payment_refund_ok_template_id = env.str(
        "PAYMENT_REFUND_OK_TEMPLATE_ID", "1824c031-cc81-4f67-aed2-f367784edc1e"
    )


config = Settings()
