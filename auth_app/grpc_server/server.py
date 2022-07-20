from concurrent import futures

import grpc

from auth_app.grpc_server import user_pb2_grpc
from auth_app.grpc_server.settings import grpc_settings
from grpc_server import user_pb2


class UserService(user_pb2_grpc.UserService):
    def GetUser(self, request, context):
        from models.db_models import User as user_model
        """Get user info from jwt token."""
        user = user_model.find_by_login(request.login)
        user_pb2.UserReply(
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
