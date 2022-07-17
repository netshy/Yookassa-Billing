from datetime import datetime

import bcrypt
import pytz


def hash_user_password(password: str) -> str:
    """Function return hashed user password."""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def check_hashed_password(hashed_password: str, password: str) -> bool:
    """Method check user's password from bd and transmitted password."""
    encoded_hash, encoded_password = hashed_password.encode(
        "utf-8"
    ), password.encode("utf-8")

    return bcrypt.checkpw(encoded_password, encoded_hash)


def get_current_date():
    return datetime.now(tz=pytz.timezone("UTC"))
