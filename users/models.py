from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', default=None, on_delete=models.CASCADE)
    code = models.CharField(max_length=50,blank=True, null=True, default=None)
    date = models.DateField(blank=True, null=True)