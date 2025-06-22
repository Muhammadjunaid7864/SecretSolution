from django.db import models
from datetime import datetime
# Create your models here.

class SealStaus(models.Model):
    sealed                  = models.BooleanField(default=False)
    threshold               = models.IntegerField()
    share                   = models.IntegerField()
    encrypted_root_token    = models.TextField()
    created_at              = models.DateField(default=datetime.now())


    def __str__(self):
        return f'{self.sealed}'