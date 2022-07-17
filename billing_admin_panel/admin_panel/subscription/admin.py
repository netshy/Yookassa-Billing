from django.contrib import admin

from subscription.models import (
    SubscriptionPlan,
    Subscription,
    Transaction,
    Refund,
)

admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)
admin.site.register(Transaction)
admin.site.register(Refund)
