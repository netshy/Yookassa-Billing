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

    try:
        rabbitmq_broker = PikaClient()
        while True:
            rabbitmq_broker.listen_events()
    finally:
        rabbitmq_broker.connection.close()


if __name__ == "__main__":
    main()
