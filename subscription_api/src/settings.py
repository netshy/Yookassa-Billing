import logging

from pydantic import BaseConfig

logger_format = "%(levelname)s %(filename)s %(asctime)s - %(message)s"

logging.basicConfig(
    filename="logfile.log",
    filemode="a",
    format=logger_format,
    level=logging.INFO
)

api_logger = logging.getLogger()
