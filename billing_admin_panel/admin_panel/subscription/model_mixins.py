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
    ACTIVE = "Active"
    ARCHIVED = "Archived"


class SubscriptionStatus(models.TextChoices):
    ACTIVE = "Active"
    EXPIRED = "Expired"


class TransactionStatus(models.TextChoices):
    PROCESSING = "Processing"
    PAID = "Paid"
    DECLINED = "Declined"


class RefundStatus(models.TextChoices):
    PROCESSING = "Processing"
    APPROVED = "Approved"
    DECLINED = "Declined"
