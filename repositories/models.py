import http
from datetime import datetime

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.dispatch import receiver

import requests

from users.models import User

from .querysets import CommitQuerySet


class Repository(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    github_id = models.IntegerField(unique=True)
    github_hook_id = models.IntegerField(unique=True, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255)

    class Meta:
        unique_together = ('name', 'user',)

    @property
    def full_name(self):
        return f'{self.user.username}/{self.name}'

    def __str__(self):
        return self.name


@receiver(models.signals.pre_delete, sender=Repository)
def repository_pre_delete(sender, instance, *args, **kwargs):  # pylint: disable=unused-argument
    if not instance.github_hook_id:
        return

    req = requests.delete(
        f'https://api.github.com/repos/{instance.full_name}/hooks/{instance.github_hook_id}',
        headers={
            'Authorization': f'token {instance.user.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    )

    if req.status_code != http.HTTPStatus.NO_CONTENT:
        raise ValueError("We cound't delete the hook, please try again later")


class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)

    sha = models.CharField(max_length=100, primary_key=True)
    url = models.CharField(max_length=255)
    created = models.DateTimeField(default=datetime.now, blank=True)
    author = JSONField()
    message = models.TextField(blank=True)

    objects = models.Manager.from_queryset(CommitQuerySet)()
