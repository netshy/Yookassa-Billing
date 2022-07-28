import backoff as backoff
import pika
from loguru import logger
from pika.exceptions import AMQPConnectionError

from api.config import config


class PikaClient:
    def __init__(self):
        self.credentials = pika.PlainCredentials(
            config.rabbit_user,
            config.rabbit_password,
        )
        self.parameters = pika.ConnectionParameters(
            config.rabbit_host,
            config.rabbit_port,
            credentials=self.credentials,
        )
        self.connection = self._connect()
        self.channel = self.connection.channel()

        self.on_channel_open()

    @backoff.on_exception(backoff.expo, AMQPConnectionError, logger=logger)
    def _connect(self):
        connection = pika.BlockingConnection(parameters=self.parameters)
        logger.info("open rabbitmq connection")
        return connection

    def on_channel_open(self):
        self.channel.confirm_delivery()
        self.channel.queue_declare(
            queue=config.rabbit_email_events_queue, durable=True
        )
        self.channel.exchange_declare(
            exchange=config.rabbit_exchange,
            durable=True,
        )
        self.channel.queue_bind(
            queue=config.rabbit_email_events_queue,
            exchange=config.rabbit_exchange,
            routing_key=config.rabbit_email_events_queue,
        )
