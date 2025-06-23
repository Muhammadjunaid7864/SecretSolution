from django.db import models
from datetime import datetime
# Create your models here.
class KvSecretPath(models.Model):
    path        = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.path

class KvSecretVersion(models.Model):
    secret_path = models.ForeignKey(KvSecretPath, on_delete=models.CASCADE)
    data        = models.JSONField()
    version     = models.IntegerField()
    created_at  = models.DateTimeField(default=datetime.now())
    deleted     = models.BooleanField(default=False)


    class Meta:
        unique_together = ("secret_path","version")
        ordering        = ["-version"]
        indexes         = [
            models.Index(fields=["secret_path"]),
        ]