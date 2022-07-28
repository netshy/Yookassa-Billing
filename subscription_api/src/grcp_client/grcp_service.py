from fastapi import Depends
from grpc._channel import Channel

from .channel import get_grcp_channel
from .schemas import BaseUser
from .user_pb2 import UserRequest
from .user_pb2_grpc import UserServiceStub


class GRCPClient:
    def __init__(self, channel: Channel):
        self.client = UserServiceStub(channel)

    def get_user_info(self, login: str):
        request = UserRequest(login=login)
        user_data = self.client.GetUser(request)
        return BaseUser(id=user_data.id, login=user_data.login, email=user_data.email)


def grcp_client_service(channel: Channel = Depends(get_grcp_channel)):
    return GRCPClient(
        channel=channel
    )
