from environs import Env
from pydantic import BaseSettings

env = Env()
env.read_env()


class Settings(BaseSettings):
    mailgun_api_key = env.str("MAILGUN_API_KEY")
    mailgun_sandbox_url = env.str("MAILGUN_SANDBOX_URL")
    mailgun_sandbox_from_email = env.str("MAILGUN_SANDBOX_FROM_EMAIL")


mailgun_config = Settings()
