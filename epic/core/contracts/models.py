from django.conf import settings
from django.db import models

from core.contacts.models import Contact


class Contract(models.Model):
    """Contract class"""

    client = models.ForeignKey(to=Contact, on_delete=models.CASCADE)
    sales = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField(default=0)
    payment_due = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
