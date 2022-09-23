from django.conf import settings
from django.db import models


class Contact(models.Model):
    """Contact class. Contact is a client or prospect"""

    sales = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, default=None)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=12, blank=True)
    mobile = models.CharField(max_length=12, blank=True)
    company_name = models.CharField(max_length=30)
    is_client = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)