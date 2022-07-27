from django.contrib import admin

from notifications.models import EmailNotification, EmailNotificationTemplate


class TemplateAdmin(admin.ModelAdmin):
    """Interface for Notification Templates."""

    pass


class EmailNotificationAdmin(admin.ModelAdmin):
    """Interface for Email Notification Templates."""

    pass


admin.site.register(EmailNotification, EmailNotificationAdmin)
admin.site.register(EmailNotificationTemplate, TemplateAdmin)
