from django.conf import settings
from django.db import models


class ClientProspect(models.Model):
    """ClientProspect class"""

    sales = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=12, blank=True)
    mobile = models.CharField(max_length=12, blank=True)
    company_name = models.CharField(max_length=30)
    is_client = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
