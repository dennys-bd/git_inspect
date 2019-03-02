from django.db import models
from django.contrib.postgres.fields import JSONField

from users.models import User

class Repository(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'user',)

class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)

    url = models.CharField(max_length=255)
    author = JSONField()
    commiter = JSONField()
    message = models.CharField(max_length=255)
