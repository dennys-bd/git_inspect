from django.db import models
from django.contrib.postgres.fields import JSONField

from users.models import User

class Repository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    github_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255)

    class Meta:
        unique_together = ('name', 'user',)

    @property
    def full_name(self):
        return f'{self.user.username}/{self.name}'

class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)

    url = models.CharField(max_length=255)
    author = JSONField()
    commiter = JSONField()
    message = models.CharField(max_length=255)
