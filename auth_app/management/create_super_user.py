import click
from flask import Blueprint

from config import ADMIN_ROLE
from db.db import sql_db
from models import User, UserRole, Role

users = Blueprint("users", __name__)


@users.cli.command("createsuperuser")
@click.argument("name")
@click.argument("password")
def create_super_user(name, password):
    is_user_exists = User.find_by_login(name)
    if is_user_exists:
        print("user already exists")
        return

    super_user = User(login=name, password=password)
    sql_db.session.add(super_user)

    role = Role.query.filter_by(role_type=ADMIN_ROLE).first()
    if not role:
        role = Role(role_type=ADMIN_ROLE)
        sql_db.session.add(role)
        sql_db.session.commit()

    user_role = UserRole(user_id=super_user.id, role_id=role.id)
    sql_db.session.add(user_role)
    sql_db.session.commit()
    print("user created")
