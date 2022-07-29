from typing import Dict

import grpc
from faker import Faker
from faker.providers import internet

from config import config
from services.grpc_client.user_pb2 import UserIDRequest
from services.grpc_client.user_pb2_grpc import UserServiceStub

fake = Faker()
fake.add_provider(internet)


class UserService:
    def get_user_info(self, user_id: str) -> Dict[str, str]:
        with grpc.insecure_channel(f"{config.grpc_url}") as channel:
            stub = UserServiceStub(channel)
            user_info = stub.GetUserByID(
                UserIDRequest(user_id=user_id)
            )
            if not user_info:
                user_info = {
                    "username": fake.name(),
                    "email": fake.email(),
                }
            else:
                user_info = {
                    "username": user_info.login,
                    "email": user_info.email,
                }
            return user_info
