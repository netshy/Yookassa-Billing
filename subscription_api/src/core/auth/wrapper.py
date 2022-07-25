import functools

from fastapi import HTTPException
from starlette import status


def login_required():
    def wrapper(func):
        @functools.wraps(func)
        async def inner(*args, **kwargs):  # noqa
            request = kwargs.get("request")
            if not getattr(request, "user", False) or not request.user.is_authenticated:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='wrong credentials')
            return await func(*args, **kwargs)
        return inner
    return wrapper
