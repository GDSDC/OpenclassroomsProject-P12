from django.conf import settings
from django.db import models

from core.clients.models import Client


class Contract(models.Model):
    """Contract class"""

    # 'client' field is required but handled by context.get('contact_id') parameter -> null=True
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE, null=True)
    sales = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField(default=0)
    payment_due = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
