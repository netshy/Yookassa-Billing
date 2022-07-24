import uuid

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID


class UUIDMixin:
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        unique=True
    )


class CustomerUUIDMixin:
    customer_id = Column()


class TimeStampedMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
