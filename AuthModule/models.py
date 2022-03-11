from django.db import models
from django.utils import timezone

# Create your models here.

class user(models.Model):
    user_id = models.AutoField
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=15)
    created_date = models.DateField(default=timezone.now)