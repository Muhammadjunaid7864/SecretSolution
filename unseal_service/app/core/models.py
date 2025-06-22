from django.db import models
from datetime import datetime
# Create your models here.

class Wraping_key(models.Model):
    wrap_key        = models.TextField()
    created_at      = models.DateField(default=datetime.now())