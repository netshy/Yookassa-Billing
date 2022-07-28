from pydantic import BaseModel


class BaseUser(BaseModel):
    id: str
    login: str
    email: str
