from enum import Enum


class NotificationType(str, Enum):
    email = "email"
    welcome_email = "welcome_email"
