from django.conf import settings
from django.db import models

from core.client_prospect.models import ClientProspect


class Event(models.Model):
    """Event class"""

    client = models.ForeignKey(to=ClientProspect, on_delete=models.CASCADE)
    support = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)
    attendees = models.IntegerField(blank=True)
    event_date = models.DateTimeField(blank=True)
    notes = models.TextField(max_length=1024, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
