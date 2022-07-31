import logging
import os

from pydantic import BaseConfig

logger_format = "%(levelname)s %(filename)s %(asctime)s - %(message)s"

logging.basicConfig(
    filename="logfile.log",
    filemode="a",
    format=logger_format,
    level=logging.INFO
)

api_logger = logging.getLogger()


class Config(BaseConfig):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    YOOKASSA_ID: str = os.getenv("YOOKASSA_ID")
    YOOKASSA_SECRET: str = os.getenv("YOOKASSA_SECRET")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")
    REFUND_NOTIFICATION_URL: str = os.getenv("REFUND_NOTIFICATION_URL")
    PAYMENT_NOTIFICATION_URL: str = os.getenv("PAYMENT_NOTIFICATION_URL")

    MIN_REFUND_DAYS = 10


billing_setting = Config()
