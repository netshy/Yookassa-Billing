from django.db import models

from billing_admin_panel.admin_panel.subscription.model_mixins import (
    UUIDMixin,
    CurrencyType,
    SubscriptionPlanStatus,
    TimeStampedMixin,
    SubscriptionStatus,
    TransactionStatus,
    RefundStatus,
)


class SubscriptionPlan(UUIDMixin):
    name = models.CharField(max_length=250)
    price = models.IntegerField()
    duration = models.IntegerField()
    currency = models.CharField(choices=CurrencyType.choices, default=CurrencyType.USD)
    status = models.CharField(
        choices=SubscriptionPlanStatus.choices, default=SubscriptionPlanStatus.ACTIVE
    )


class Subscription(UUIDMixin, TimeStampedMixin):
    plan_id = models.ForeignKey(
        "SubscriptionPlan", on_delete=models.CASCADE, related_name="subscriptions"
    )
    customer_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="subscriptions"
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(
        choices=SubscriptionStatus.choices, default=SubscriptionStatus.ACTIVE
    )


class Transaction(UUIDMixin):
    plan_id = models.ForeignKey(
        "SubscriptionPlan", on_delete=models.CASCADE, related_name="transactions"
    )
    customer_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="transactions"
    )
    session_id = models.TextField()
    status = models.CharField(
        choices=TransactionStatus.choices, default=TransactionStatus.PROCESSING
    )


class Refund(UUIDMixin, TimeStampedMixin):
    customer_id = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="refunds"
    )
    transaction_id = models.ForeignKey(
        "Transaction", on_delete=models.CASCADE, related_name="refunds"
    )
    amount = models.IntegerField()
    status = models.CharField(
        choices=RefundStatus.choices, default=RefundStatus.PROCESSING
    )
