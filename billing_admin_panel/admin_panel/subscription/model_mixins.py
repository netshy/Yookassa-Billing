import uuid

from django.db import models


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.id

    class Meta:
        abstract = True


class CustomerUUIDMixin(models.Model):
    customer_id = models.UUIDField()

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CurrencyType(models.TextChoices):
    USD = "USD"
    RUB = "RUB"


class SubscriptionPlanStatus(models.TextChoices):
    ACTIVE = "active"
    ARCHIVED = "archived"


class SubscriptionPlanType(models.TextChoices):
    BASIC = "basic"
    OPTIONAL = "optional"


class SubscriptionStatus(models.TextChoices):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class TransactionStatus(models.TextChoices):
    PROCESSING = "processing"
    PAID = "paid"
    DECLINED = "declined"


class RefundStatus(models.TextChoices):
    PROCESSING = "processing"
    APPROVED = "approved"
    DECLINED = "declined"
