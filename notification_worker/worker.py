import logging

from jinja2 import Environment
from loguru import logger

from db.pg_service import PostgresHelper
from services.email_sender_service import EmailSenderService
from services.film_service import FilmService
from models.email_event import EmailEvent
from models.hello_event import HelloEvent
from services.user_service import UserService


class Worker:
    def __init__(
        self,
        pgh: PostgresHelper,
        user_service: UserService,
        film_service: FilmService,
        email_sender: EmailSenderService,
    ):
        self.pgh = pgh
        self.user_service = user_service
        self.film_service = film_service
        self.email_sender = email_sender

    def _get_template(self, template_id: str):
        template = self.pgh.get_template_html(template_id)
        return template

    def handle_email_event(self, notification: EmailEvent):
        template_db = self._get_template(notification.template_id)
        if not template_db:
            logger.error(f"template {notification.template_id} not found")
            return
        else:
            template_db = template_db[0]

        film_names = [
            self.film_service.get_film_name(film_id)
            for film_id in notification.data.film_ids
        ]
        film_names = ", ".join(film_names)
        for user_id in notification.data.user_ids:
            user_info = self.user_service.get_user_info(user_id)

            context = {
                "username": user_info["username"],
                "film_names": film_names,
            }
            complete_template = self._get_notification_html(
                template_db["template_data"], context
            )
            self.email_sender.send_email(
                to=user_info["email"],
                subject=template_db["subject"],
                html=complete_template,
            )
            logging.info(f"Send event notification email to {user_id}")

    def handle_hello_event(self, notification: HelloEvent):
        template_db = self._get_template(notification.template_id)
        if not template_db:
            logger.error(f"template {notification.template_id} not found")
            return
        else:
            template_db = template_db[0]

        user_info = self.user_service.get_user_info(notification.user_id)
        context = {
            "username": user_info["username"],
            "email": user_info["email"],
        }
        complete_template = self._get_notification_html(
            template_db["template_data"], context
        )
        self.email_sender.send_email(
            to=user_info["email"],
            subject=template_db["subject"],
            html=complete_template,
        )
        logging.info(f"Send welcome email to {notification.user_id}")

    @staticmethod
    def _get_notification_html(template_html, context):
        env = Environment(autoescape=True)
        template_obj = env.from_string(template_html)
        return template_obj.render(**context)
