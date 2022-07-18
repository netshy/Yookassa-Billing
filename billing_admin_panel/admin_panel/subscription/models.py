import uuid

from django.db import models

from subscription.model_mixins import (
    UUIDMixin,
    CurrencyType,
    SubscriptionPlanStatus,
    TimeStampedMixin,
    SubscriptionStatus,
    TransactionStatus,
    RefundStatus,
    CustomerUUIDMixin,
    SubscriptionPlanType,
)


class SubscriptionPlan(UUIDMixin):
    name = models.CharField(max_length=250)
    price = models.IntegerField()
    duration = models.IntegerField()
    currency = models.CharField(
        choices=CurrencyType.choices, default=CurrencyType.RUB, max_length=10
    )
    status = models.CharField(
        choices=SubscriptionPlanStatus.choices,
        default=SubscriptionPlanStatus.ACTIVE,
        max_length=100,
    )
    type = models.CharField(
        choices=SubscriptionPlanType.choices,
        default=SubscriptionPlanType.BASIC,
        max_length=30
    )

    class Meta:
        db_table = "subscription_plan"

    def __str__(self):
        return f"Subscription Plan: {self.name}. Cost: {self.price} {self.currency}"


class Subscription(UUIDMixin, CustomerUUIDMixin, TimeStampedMixin):
    plan_id = models.ForeignKey(
        "SubscriptionPlan", on_delete=models.CASCADE, related_name="subscriptions"
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.ACTIVE,
        max_length=100,
    )

    class Meta:
        db_table = "subscription"

    def __str__(self):
        return f"Subscription: {self.id} for customer id: {self.customer_id}"


class Transaction(UUIDMixin, CustomerUUIDMixin):
    plan_id = models.ForeignKey(
        "SubscriptionPlan", on_delete=models.CASCADE, related_name="transactions"
    )
    session_id = models.TextField()
    status = models.CharField(
        choices=TransactionStatus.choices,
        default=TransactionStatus.PROCESSING,
        max_length=100,
    )
    idempotence_key = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        db_table = "transaction"

    def __str__(self):
        return f"Transaction: {self.id} for customer: {self.customer_id}. Status: {self.status}"


class Refund(UUIDMixin, CustomerUUIDMixin, TimeStampedMixin):
    transaction_id = models.ForeignKey(
        "Transaction", on_delete=models.CASCADE, related_name="refunds"
    )
    amount = models.IntegerField()
    status = models.CharField(
        choices=RefundStatus.choices, default=RefundStatus.PROCESSING, max_length=100
    )

    class Meta:
        db_table = "refund"

    def __str__(self):
        return (
            f"Refund for customer id: {self.customer_id}. Transaction id: {self.transaction_id}. "
            f"Amount: {self.amount}. Status: {self.status}"
        )
