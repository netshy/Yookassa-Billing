import uuid

from sqlalchemy import func, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID


class BaseModelMixin(object):
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())
