from loguru import logger

from config import config
from db.pg_service import PostgresConnector, PostgresHelper
from services.film_service import FilmService

from worker import Worker
from services.email_sender_service import EmailSenderService
from services.user_service import UserService

pg = PostgresConnector(config.pg_dsl)
pgh = PostgresHelper(pg.cursor)
worker = Worker(
    pgh=pgh,
    user_service=UserService(),
    film_service=FilmService(),
    email_sender=EmailSenderService(),
)


def main():
    from rabbimq import PikaClient

    rabbitmq_broker = PikaClient()
    rabbitmq_broker.consume()
    try:
        rabbitmq_broker.listen_events()
    except Exception as err:
        logger.error('pika error:', err)
        rabbitmq_broker.channel.stop_consuming()


if __name__ == "__main__":
    main()
