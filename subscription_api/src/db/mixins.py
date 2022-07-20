from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID


class UUIDMixin:
    id = Column(UUID, primary_key=True, index=True)


class CustomerUUIDMixin:
    id = Column(UUID)


class TimeStampedMixin:
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
