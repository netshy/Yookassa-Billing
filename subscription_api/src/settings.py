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


billing_setting = Config()
