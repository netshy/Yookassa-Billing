from environs import Env

env = Env()
env.read_env()

ADMIN_ROLE = "ADMIN"


class Config:
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{env.str("DB_USER")}:{env.str("DB_PASSWORD")}@'
        f'{env.str("DB_HOST")}:{env.int("DB_PORT")}/{env.str("DB_NAME")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = env.str("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = env.timedelta("JWT_ACCESS_TOKEN_EXPIRES", 3600)
    JWT_REFRESH_TOKEN_EXPIRES = env.timedelta("JWT_REFRESH_TOKEN_EXPIRES", False)
    PROPAGATE_EXCEPTIONS = True

    REDIS_HOST = env.str("REDIS_HOST")
    REDIS_PORT = env.int("REDIS_PORT")
    REDIS_PASSWORD = env.str("REDIS_PASSWORD")
