from pydantic import BaseSettings


class Settings(BaseSettings):
    GRPC_PORT: int = 50055


grpc_settings = Settings()
