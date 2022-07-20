from concurrent import futures

import grpc

import user_pb2
import user_pb2_grpc
from settings import grpc_settings


class UserService(user_pb2_grpc.UserService):
    def GetUser(self, request, context):
        from models import User
        """Get user info from jwt token."""
        user = User.find_by_login(request.login)
        return user_pb2.UserReply(
            id=user.id,
            login=user.login,
            first_name=user.first_name,
            last_name=user.last_name
        )


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port(f"[::]:{grpc_settings.GRPC_PORT}")
    server.start()
    server.wait_for_termination()
