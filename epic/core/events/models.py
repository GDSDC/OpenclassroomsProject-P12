from django.conf import settings
from django.db import models

from core.clients.models import Client


class Event(models.Model):
    """Event class"""

    # 'client' field is required but handled by context.get('contact_id') parameter -> null=True
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE, null=True)
    support = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)
    attendees = models.IntegerField(default=0)
    event_date = models.DateTimeField()
    notes = models.TextField(max_length=1024, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
