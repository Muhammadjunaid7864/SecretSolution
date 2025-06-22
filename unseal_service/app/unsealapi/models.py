from django.db import models
from datetime import datetime
# Create your models here.

class SealStatus(models.Model):
    seal        = models.BooleanField(default=False)
    threshold   = models.IntegerField()
    share       = models.IntegerField(default=0)
    unseal_key  = models.JSONField(default=list)
    root_token  = models.TextField()
    created_at  = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f'{self.created_at}'

