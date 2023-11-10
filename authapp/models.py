from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add additional fields here
    age = models.IntegerField(null=True, blank=True)
    # You can add other custom fields as needed