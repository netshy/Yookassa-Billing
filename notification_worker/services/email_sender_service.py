import requests
from loguru import logger

from services.mailgun_config import mailgun_config


class EmailSenderService:
    def send_email(self, to, subject, body) -> int:
        """method send email notification."""
        authentication = ("api", mailgun_config.mailgun_api_key)
        data = {
            "from": mailgun_config.mailgun_sandbox_from_email,
            "to": to,
            "subject": subject,
            "text": body,
        }
        result = requests.post(
            mailgun_config.mailgun_sandbox_url, auth=authentication, data=data
        )
        logger.info(f'send mail to {to}, status: {result.status_code}')
        return result.status_code
