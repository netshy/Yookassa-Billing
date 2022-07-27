import backoff as backoff
import pika
from loguru import logger
from orjson import orjson
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPConnectionError

from config import config
from main import worker
from models.choices import NotificationType
from models.email_event import EmailEvent
from models.hello_event import HelloEvent


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

    @staticmethod
    def handle_event_callback(
        ch: BlockingChannel, method, properties, body: bytes
    ):
        event_data = orjson.loads(body)
        event_type = event_data["type"]
        events_model = {
            NotificationType.email: (EmailEvent, worker.handle_email_event),
            NotificationType.welcome_email: (
                HelloEvent,
                worker.handle_hello_event,
            ),
        }
        event_model, func = events_model[event_type]
        notification = event_model(**event_data)
        func(notification)

    def listen_events(self):
        self.channel.basic_consume(
            queue=config.rabbit_email_events_queue,
            on_message_callback=self.handle_event_callback,
            auto_ack=True,
        )
        logger.info(f"listen queue: {config.rabbit_email_events_queue}")
        self.channel.start_consuming()
