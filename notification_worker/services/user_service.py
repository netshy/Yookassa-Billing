from typing import Dict

import grpc
from faker import Faker
from faker.providers import internet

from config import config
from services.grpc_client import user_pb2, user_pb2_grpc

fake = Faker()
fake.add_provider(internet)


class UserService:
    def get_user_info(self, user_id: str) -> Dict[str, str]:
        with grpc.insecure_channel(f"{config.grpc_url}") as channel:
            stub = user_pb2_grpc.UserStub(channel)
            user_info = stub.GetName(
                user_pb2.ProfileInfoRequest(user_id=user_id)
            )
            if not user_info:
                user_info = {
                    "username": fake.name(),
                    "email": fake.email(),
                }
            return user_info
