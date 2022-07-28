import uuid

from django.db import models


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.id

    class Meta:
        abstract = True


class BaseDateTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NotificationType(models.TextChoices):
    undefined = "undefined", "notification type undefined"
    email = "email", "email notification"
    sms = "sms", "sms notification"


class EmailNotificationTemplate(UUIDMixin, BaseDateTime):
    class EmailTemplateType(models.TextChoices):
        advertisement = "advertisement", "advertisement email"
        personal = "personal", "personal email"

    template_type = models.CharField(
        choices=EmailTemplateType.choices, max_length=100
    )
    subject = models.CharField(max_length=500)
    # Jinja2 template, store 'html' template
    template_data = models.TextField()

    def __str__(self):
        return f"Notification: {self.subject} - {self.id}"

    class Meta:
        db_table = "notification_template"


class EmailNotification(UUIDMixin, BaseDateTime):
    class NotificationStatus(models.TextChoices):
        cancelled = "cancelled", "notification cancelled"
        pending = "pending", "waiting to send"
        sent = "sent", "notification sent"

    # example data https://www.laurencegellert.com/2018/09/django-tricks-for-processing-and-storing-json/  # noqa
    data = models.JSONField(
        verbose_name="store data in json, transmit into template"
    )
    title = models.TextField(verbose_name="Email notification title")
    subject = models.TextField(verbose_name="Email subject")
    template = models.ForeignKey(
        EmailNotificationTemplate,
        on_delete=models.CASCADE,
        related_name="email_notifications",
    )
    status = models.CharField(
        choices=NotificationStatus.choices,
        default=NotificationStatus.pending,
        max_length=100,
    )
    scheduled_time = models.DateTimeField()
    is_advertisement = models.BooleanField(
        verbose_name="Is ad or not. User can disable ad emails.", default=False
    )
    type = models.CharField(default=NotificationType.email, max_length=100)

    def __str__(self):
        return f"Notification: {self.type} - {self.id}"

    class Meta:
        db_table = "email_notification"
