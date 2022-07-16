from django.contrib import admin

from subscription.models import (
    SubscriptionPlan,
    Subscription,
    Transaction,
    Refund,
    User
)

admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)
admin.site.register(Transaction)
admin.site.register(Refund)
admin.site.register(User)