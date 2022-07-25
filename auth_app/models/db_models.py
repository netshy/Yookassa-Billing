from sqlalchemy.dialects.postgresql import UUID

from db.db import sql_db
from models.model_mixins import BaseModelMixin
from models.utils import hash_user_password, check_hashed_password


class User(BaseModelMixin, sql_db.Model):
    __tablename__ = "users"

    login = sql_db.Column(sql_db.String, unique=True, nullable=False)
    password = sql_db.Column(sql_db.String, nullable=False)
    email = sql_db.Column(sql_db.String, nullable=False, unique=True)

    def __init__(self, login, password, email):
        self.login = login
        self.password = hash_user_password(password)
        self.email = email

    def __repr__(self):
        return f"<User {self.login}>"

    def check_user_password(self, password_to_check):
        return check_hashed_password(self.password, password_to_check)

    def get_all_roles(self):
        raw_user_roles = (
            Role.query.join(UserRole).filter(UserRole.user_id == self.id).all()
        )
        result = [role.role_type for role in raw_user_roles]
        return result

    @classmethod
    def find_by_login(cls, login: str):
        # Trying to find user by it's login
        # https://stackoverflow.com/a/8934748
        return cls.query.filter_by(login=login).first()\

    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, user_id: str):
        return cls.query.filter_by(id=user_id).one_or_none()


class Role(BaseModelMixin, sql_db.Model):
    __tablename__ = "roles"

    role_type = sql_db.Column(sql_db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Role {self.role_type}>"

    @classmethod
    def role_is_exist(cls, role_name: str):
        """Method return if Role is already exists or not."""
        # https://stackoverflow.com/a/37483741
        return sql_db.session.query(
            cls.query.filter_by(role_type=role_name).exists()
        ).scalar()


class UserRole(BaseModelMixin, sql_db.Model):
    __tablename__ = "user_role"

    user_id = sql_db.Column(UUID(as_uuid=True), sql_db.ForeignKey("users.id"))
    role_id = sql_db.Column(UUID(as_uuid=True), sql_db.ForeignKey("roles.id"))

    @classmethod
    def is_user_role_exist(cls, user_id: str, role_id: str) -> bool:
        return sql_db.session.query(
            cls.query.filter_by(user_id=user_id, role_id=role_id).exists()
        ).scalar()


class RolePermission(BaseModelMixin, sql_db.Model):
    __tablename__ = "roles_permissions"

    role_id = sql_db.Column(
        UUID(as_uuid=True), sql_db.ForeignKey("roles.id"), nullable=False
    )
    permission_id = sql_db.Column(
        UUID(as_uuid=True), sql_db.ForeignKey("permissions.id"), nullable=False
    )


class Permission(BaseModelMixin, sql_db.Model):
    __tablename__ = "permissions"

    permission_type = sql_db.Column(sql_db.String, unique=True, nullable=False)


class Session(BaseModelMixin, sql_db.Model):
    __tablename__ = "sessions"

    user_id = sql_db.Column(
        UUID(as_uuid=True), sql_db.ForeignKey("users.id"), nullable=False
    )
    user_agent = sql_db.Column(sql_db.String, nullable=False)

    @classmethod
    def find_by_user_and_agent(cls, user_id: str, user_agent):
        """Method looking for a existed user session."""
        return cls.query.filter_by(
            user_id=user_id, user_agent=user_agent
        ).one_or_none()






