from concurrent import futures

import grpc

import user_pb2
import user_pb2_grpc
from settings import grpc_settings


class UserService(user_pb2_grpc.UserService):
    def GetUser(self, request, context):
        """Get user info from jwt token."""
        # https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/

        from auth import create_app
        app = create_app()
        with app.app_context():
            from models import User

            user = User.find_by_login(request.login)
            if not user:
                return user_pb2.UserReply(
                    id=None,
                    login=None,
                    first_name=None,
                    last_name=None
                )
            return user_pb2.UserReply(
                id=str(user.id),
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
