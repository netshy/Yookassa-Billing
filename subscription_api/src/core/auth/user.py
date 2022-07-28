from pydantic import BaseModel


class User(BaseModel):
    id: str
    login: str
    email: str

    @property
    def is_authenticated(self) -> bool:
        return True
