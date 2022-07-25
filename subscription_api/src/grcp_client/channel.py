from typing import Optional

from grpc._channel import Channel

grcp_channel: Optional[Channel] = None


def get_grcp_channel():
    return grcp_channel
